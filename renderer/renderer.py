import numpy as np
import time

import screen

display = screen.Screen(150, 80)

vertexBuffer = [
    np.array([-1, -1, -1, 1]),
    np.array([-1, -1, 1, 1]),
    np.array([-1, 1, -1, 1]),
    np.array([-1, 1, 1, 1]),
    np.array([1, -1, -1, 1]),
    np.array([1, -1, 1, 1]),
    np.array([1, 1, -1, 1]),
    np.array([1, 1, 1, 1])
]

edgeBuffer = [
    (0, 1),
    (0, 2),
    (0, 4),
    (1, 3),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 6),
    (5, 7),
    (6, 7)
]

view = np.identity(4)

f = 1
zNear = 1
zFar = 10
aspect = display.width / display.height
projection = np.array([
    [f / aspect, 0,                               0,                                   0],
    [         0, f,                               0,                                   0],
    [         0, 0, (zFar + zNear) / (zNear - zFar), (2 * zFar * zNear) / (zNear - zFar)],
    [         0, 0,                              -1,                                   0]
])

projectedVertexBuffer = []

def main():
    startTime = time.time()
    global display
    while True:
        display.clear()
        updateProjectedVertexBuffer()
        angle = (time.time() - startTime)
        updateViewMatrix(angle, 4)
        drawVertices([0, 1, 2, 3, 4, 5, 6, 7])
        drawTriangle(0, 1, 2)
        print(display)
        print(angle)
        time.sleep(0.1)

def drawVertices(vertices):
    for vertex in vertices:
        vertex = projectedVertexBuffer[vertex]
        try:
            screenX = int((vertex[0] + 1) * 0.5 * display.width)
            screenY = int((vertex[1] + 1) * 0.5 * display.height)
        except:
            screenX = -1
            screenY = -1
        if screenX < 0 or screenX >= display.width or screenY < 0 or screenY >= display.height:
            continue
        display.pixels[screenY][screenX] = 1

def drawTriangle(a, b, c):
    a = projectedVertexBuffer[a]
    b = projectedVertexBuffer[b]
    c = projectedVertexBuffer[c]

    minX = np.floor(min(a[0], b[0], c[0]))
    maxX = np.ceil(max(a[0], b[0], c[0]))
    minY = np.floor(min(a[1], b[1], c[1]))
    maxY = np.ceil(max(a[1], b[1], c[1]))

    area = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

    for px in range(int(minX), int(maxX)):
        for py in range(int(minY), int(maxY)):
            weightA = ((b[0] - c[0]) * (py - c[1]) + (c[1] - b[1]) * (px - c[0])) / area
            weightB = ((c[0] - a[0]) * (py - a[1]) + (a[1] - c[1]) * (px - a[0])) / area
            weightC = 1 - weightA - weightB

            print(weightA, weightB, weightC)

            if weightA >= 0 and weightB >= 0 and weightC >= 0 and weightA <= 1 and weightB <= 1 and weightC <= 1:
                display.pixels[px][py] = 1
            else:
                display.pixels[px][py] = 0

def updateViewMatrix(angle, radius):
    global view

    rotation = np.array([
        [ np.cos(angle), 0, np.sin(angle), 0],
        [             0, 1,             0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [             0, 0,             0, 1]
    ])

    translation = np.array([
        [1, 0, 0, radius * np.sin(angle)],
        [0, 1, 0, np.sin(angle) * 2],
        [0, 0, 1, -radius * np.cos(angle)],
        [0, 0, 0, 1]
    ])

    view = np.dot(rotation, translation)

def updateProjectedVertexBuffer():
    global projectedVertexBuffer
    projectedVertexBuffer = []
    for vertex in vertexBuffer:
        cameraVertex = np.dot(view, vertex)
        projectedVertex = np.dot(projection, cameraVertex)
        projectedVertex /= projectedVertex[3]
        projectedVertexBuffer.append(projectedVertex)
    projectedVertexBuffer = np.array(projectedVertexBuffer)

if __name__ == "__main__":
    main()
