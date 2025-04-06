class Screen:
    width = 0
    height = 0
    pixels = []

    def __init__(self, width, height):
        self.width = width
        self.height = height
        for x in range(height):
            row = []
            for y in range(width):
                row.append(0)
            self.pixels.append(row)

    def clear(self):
        for x in range(self.height):
            for y in range(self.width):
                self.pixels[x][y] = 0

    def __str__(self):
        display = ""
        display = display + "┏" + "━" * (self.width * 2) + "┓\n"
        for x in range(self.height):
            display = display + "┃"
            for y in range(self.width):
                display = display + str("  " if self.pixels[x][y] == 0 else "██")
            display = display + "┃\n"
        display = display + "┗" + "━" * (self.width * 2) + "┛\n"
        return display
