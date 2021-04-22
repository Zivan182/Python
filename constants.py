"""Константы

Constants
--------
WIDTH : int
    ширина поля
HEIGHT : int
    высота поля
BG_COLOR : str
    цвет поля
SMALL_CONSTANT : float
    маленькая константа
BULLET_R : float
    радиус пули
BULLET_COLOR : str
    цвет пули
WALL_COLOR : str
    цвет стены
TANK_COLOR1 :str
    цвет первого танка
TANK_COLOR2 : str
    цвет второго танка
OUTLINE1 : str
    цвет границы первого танка
OUTLINE2 :str
    цвет границы второго танка
WALL_LEN : float
    длина стены
STEP : float
    шаг
ANGLE : float
    угол поворота
N : int
    HEIGHT/WALL_LEN
M : int
    WIDTH/WALL_LEN

vertical_walls : list
    список вертикальных стен
horizontal_walls : list
    список горизонтальных стен
bullets : list
    список пуль
"""

WIDTH = 1200
HEIGHT = 600
BG_COLOR = 'white'
SMALL_CONSTANT = 0.2
BULLET_R = 4
BULLET_COLOR = 'black'
WALL_COLOR = 'purple'
TANK_COLOR1 = 'red'
TANK_COLOR2 = 'green'
OUTLINE1 = 'black'
OUTLINE2 = 'black'
WALL_LEN = 60
STEP = 1.2
ANGLE = 0.1
N = 10
M = 20

vertical_walls = []
horizontal_walls = []
bullets = []
