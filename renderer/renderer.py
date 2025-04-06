import numpy as np
import time

import screen

display = screen.Screen(120, 50)

vertexBuffer = [
    np.array([-1, -1, -1, 1]),
    np.array([-1, -1, 1, 1]),
    np.array([-1, 1, -1, 1]),
    np.array([-1, 1, 1, 1]),
    np.array([1, -1, -1, 1]),
    np.array([1, -1, 1, 1]),
    np.array([1, 1, -1, 1]),
    np.array([1, 1, 1, 1]),]

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
        [0, 1, 0, angle / 4 - 5],
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
