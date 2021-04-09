import math
from wall import *
from geometry import *
from variables import *


class bullet():
    def __init__(self, canvas, x, y, dx, dy, r = BULLET_R, color = BULLET_COLOR):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy
        self.id = self.canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = BULLET_COLOR)
        self.live = True
        self.canvas.after(10000, self.stop)
        self.move()


    def collision(self):
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
        self.live = False
        self.canvas.move(self.id, 2000, 2000)


    def move(self):
        if self.live:
            self.collision()
            self.canvas.move(self.id, self.dx, self.dy)
            self.x += self.dx
            self.y += self.dy
            self.canvas.after(30, self.move)
