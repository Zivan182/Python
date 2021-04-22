from abc import abstractmethod
from constants import *

class Wall():
    """ Класс Wall - стена

    Attributes
    ----------
    x, y : float
        координаты левой верхней вершины
    len : float
        длина стены
    color : str
        цвет стены

    Methods
    -------
    @abstractmethod
    draw()
    """

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
    """Класс VerticalWall - вертикальная стена
    наследуется от класса Wall

    Methods
    -------
    draw()
        рисует стену
    """

    def __init__(self, canvas, x, y, len = WALL_LEN, color = WALL_COLOR):
        Wall.__init__(self, canvas, x, y, len, color)
        self.draw()


    def draw(self):
        self.canvas.create_line(self.x, self.y, self.x, self.y + self.len, fill=WALL_COLOR)


class HorizontalWall(Wall):
    """Класс HorizontalWall - горизонтальная стена
    наследуется от класса Wall

    Methods
    -------
    draw()
        рисует стену
    """

    def __init__(self, canvas, x, y, len = WALL_LEN, color = WALL_COLOR):
        Wall.__init__(self, canvas, x, y, len, color)
        self.draw()


    def draw(self):
        self.canvas.create_line(self.x, self.y, self.x + self.len, self.y, fill=WALL_COLOR)
