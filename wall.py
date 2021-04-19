from abc import abstractmethod
from variables import *

class Wall():
    def __init__(self, canvas, x, y, len, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.len = len
        self.color = color

    @abstractmethod
    def draw(self):
        pass

class VerticalWall(Wall):
    def __init__(self, canvas, x, y, len = WALL_LEN, color = WALL_COLOR):
        Wall.__init__(self, canvas, x, y, len, color)
        self.draw()


    def draw(self):
        self.canvas.create_line(self.x, self.y, self.x, self.y + self.len, fill=WALL_COLOR)


class HorizontalWall(Wall):
    def __init__(self, canvas, x, y, len = WALL_LEN, color = WALL_COLOR):
        Wall.__init__(self, canvas, x, y, len, color)
        self.draw()


    def draw(self):
        self.canvas.create_line(self.x, self.y, self.x + self.len, self.y, fill=WALL_COLOR)
