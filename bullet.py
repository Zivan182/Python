import math
from wall import *
from geometry import *
from constants import *


class Bullet():
    """ Класс Bullet - пуля

    Attributes
    ----------
    x, y : float
        координаты центра
    r : float, optional
        радиус
    dx, dy : float
        смещение пули по осям Ox/Oy при движении
    color : str, optional
        цвет пули
    live : bool
        индикатор жизни пули
    stopped : bool
        индикатор движения пули

    Methods
    -------
    collision()
        проверяет столкновения пули со стенами
    stop()
        вызывается через 10s после создания пули;
        устанавливает False значением индикатора live, переносит пулю за пределы поля
    move()
        вызывается при создании пули;
        вызывает метод collision();
        производит движение пули в соответствии с индикатором live;
        обновляет координаты центра;
        вызывает себя снова через 30ms
    """

    def __init__(self, canvas, x, y, dx, dy, r = BULLET_R, color = BULLET_COLOR):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy
        self.id = self.canvas.create_oval(self.x - self.r, self.y - self.r,
                                          self.x + self.r, self.y + self.r, fill = BULLET_COLOR)
        self.live = True
        self.stopped = False
        self.canvas.after(10000, self.stop)
        self.move()


    def collision(self):
        """проверяет столкновения пули со стенами"""

        for v_wall in vertical_walls:
            if (abs(v_wall.x - self.x) <= self.r + 2) and (v_wall.y <= self.y <= v_wall.y + v_wall.len):
                self.dx = -self.dx
            elif distance(self.x, self.y, v_wall.x, v_wall.y) <= self.r + 2:
                self.dy = -self.dy
            elif distance(self.x, self.y, v_wall.x, v_wall.y + v_wall.len) <= self.r + 2:
                self.dy = -self.dy
        for h_wall in horizontal_walls:
            if (abs(h_wall.y - self.y) <= self.r + 2) and (h_wall.x <= self.x <= h_wall.x + h_wall.len):
                self.dy = -self.dy
            elif distance(self.x, self.y, v_wall.x, v_wall.y) <= self.r + 2:
                self.dx = -self.dx
            elif distance(self.x, self.y, h_wall.x + h_wall.len, h_wall.y) <= self.r + 2:
                self.dx = -self.dx


    def stop(self):
        """вызывается через 10s после создания пули;
        устанавливает False значением индикатора live, переносит пулю за пределы поля
        """

        self.live = False
        self.canvas.move(self.id, 2000, 2000)


    def move(self):
        """вызывается при создании пули;
        вызывает метод collision();
        производит движение пули в соответствии с индикатором live;
        обновляет координаты центра;
        вызывает себя снова через 30ms
        """

        if self.live and not self.stopped:
            self.collision()
            self.canvas.move(self.id, self.dx, self.dy)
            self.x += self.dx
            self.y += self.dy
            self.canvas.after(30, self.move)
