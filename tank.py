import math
import time
from wall import *
from bullet import *
from geometry import *
from variables import *


class tank():
    def __init__(self, canvas, points, color):
        self.canvas = canvas
        self.points = points
        self.update()
        self.color = color
        self.id = self.canvas.create_polygon(self.points, fill=color, outline=OUTLINE1)
        self.bullets = 0
        self.pressed = {'forward': False, 'left': False, 'backward': False, 'right': False, 'fire': False}


    def update(self):
        self.A = self.points[0]
        self.B = self.points[1]
        self.C = self.points[2]
        self.D = self.points[3]
        self.O = [(self.A[0] + self.C[0]) / 2, (self.A[1] + self.C[1]) / 2]
        self.muzzle = [(self.A[0] + self.B[0]) / 2, (self.A[1] + self.B[1]) / 2]
        self.dx = (self.muzzle[0] - self.O[0]) * SMALL_CONSTANT
        self.dy = (self.muzzle[1] - self.O[1]) * SMALL_CONSTANT


    def collision(self):
        for v_wall in vertical_walls:
            begin = [v_wall.x, v_wall.y]
            end = [v_wall.x, v_wall.y + v_wall.len]
            xab, yab = intersect(self.A, self.B, begin, end)
            zdvc, wegw = intersect(self.B, self.C, begin, end)
            xcd, ycd = intersect(self.C, self.D, begin, end)
            xda, yda = intersect(self.D, self.A, begin, end)
            if (begin[1] <= yab <= end[1] and (self.A[0] - xab)*(self.B[0]-xab)<=0) or \
                    (begin[1] <= wegw <= end[1] and (self.B[0] - zdvc)*(self.C[0]-zdvc)<=0) or \
                    (begin[1] <= ycd <= end[1] and (self.C[0] - xcd)*(self.D[0]-xcd)<=0) or \
                    (begin[1] <= yda <= end[1] and (self.D[0] - xda)*(self.A[0]-xda)<=0):
                return v_wall
        for h_wall in horizontal_walls:
            begin = [h_wall.x, h_wall.y]
            end = [h_wall.x + h_wall.len, h_wall.y]
            xab, yab = intersect(self.A, self.B, begin, end)
            zdvs, wegw = intersect(self.B, self.C, begin, end)
            xcd, ycd = intersect(self.C, self.D, begin, end)
            xda, yda = intersect(self.D, self.A, begin, end)
            if (begin[0] <= xab <= end[0] and (self.A[1] - yab) * (self.B[1] - yab) <= 0) or \
                    (begin[0] <= zdvs <= end[0] and (self.B[1] - wegw) * (self.C[1] - wegw) <= 0) or \
                    (begin[0] <= xcd <= end[0] and (self.C[1] - ycd) * (self.D[1] - ycd) <= 0) or \
                    (begin[0] <= xda <= end[0] and (self.D[1] - yda) * (self.A[1] - yda) <= 0):
                return h_wall
        return False


    def move_forward(self):
        self.canvas.move(self.id, self.dx, self.dy)
        for i in range(4):
            self.points[i][0] += self.dx
            self.points[i][1] += self.dy
        self.update()


    def move_backward(self):
        self.canvas.move(self.id, -self.dx, -self.dy)
        for i in range(4):
            self.points[i][0] -= self.dx
            self.points[i][1] -= self.dy
        self.update()


    def rotate_left(self, angle=ANGLE):
        s = math.sin(angle)
        c = math.cos(angle)
        self.canvas.create_polygon(self.points, fill=BG_COLOR, outline=BG_COLOR)
        for i in range(4):
            x, y = self.points[i]
            self.points[i][0] = self.O[0] + c * (x - self.O[0]) + s * (y - self.O[1])
            self.points[i][1] = self.O[1] - s * (x - self.O[0]) + c * (y - self.O[1])
        self.id = self.canvas.create_polygon(self.points, fill=self.color, outline=OUTLINE1)
        self.update()


    def rotate_right(self, angle=ANGLE):
        s = math.sin(angle)
        c = math.cos(angle)
        self.canvas.create_polygon(self.points, fill=BG_COLOR, outline=BG_COLOR)
        for i in range(4):
            x, y = self.points[i]
            self.points[i][0] = self.O[0] + c * (x - self.O[0]) - s * (y - self.O[1])
            self.points[i][1] = self.O[1] + s * (x - self.O[0]) + c * (y - self.O[1])
        self.id = self.canvas.create_polygon(self.points, fill=self.color, outline=OUTLINE1)
        self.update()


    def bullet_delete(self):
        self.bullets -= 1


    def fire(self):
        if self.bullets < 5:
            tank_bullet = bullet(self.canvas, self.muzzle[0] + STEP * self.dx, self.muzzle[1] + STEP * self.dy, 2 * self.dx,
                                 2 * self.dy)
            self.bullets += 1
            bullets.append(tank_bullet)
            self.canvas.after(10000, self.bullet_delete)


    def died(self):
        for bull in bullets:
            if distance(self.O[0], self.O[1], bull.x, bull.y) <= bull.r + 15:
                time.sleep(3)
                self.canvas.quit()
        self.canvas.after(30, self.died)


    def press_forward(self, event):
        self.pressed['forward'] = True


    def release_forward(self, event):
        self.pressed['forward'] = False


    def press_left(self, event):
        self.pressed['left'] = True


    def release_left(self, event):
        self.pressed['left'] = False


    def press_backward(self, event):
        self.pressed['backward'] = True


    def release_backward(self, event):
        self.pressed['backward'] = False


    def press_right(self, event):
        self.pressed['right'] = True


    def release_right(self, event):
        self.pressed['right'] = False


    def press_fire(self, event):
        self.pressed['fire'] = True


    def release_fire(self, event):
        self.pressed['fire'] = False


    def f(self):
        if (self.pressed['fire']):
            self.fire()
        self.canvas.after(200, self.f)


    def move(self):
        if (self.pressed['forward']):
            self.move_forward()
            if self.collision():
                self.move_backward()
        if (self.pressed['backward']):
            self.move_backward()
            if self.collision():
                self.move_forward()
        if (self.pressed['left']):
            self.rotate_left()
            w = self.collision()
            if w is not False:
                self.rotate_right()
                w.draw()
        if (self.pressed['right']):
            self.rotate_right()
            w = self.collision()
            if w is not False:
                self.rotate_left()
                w.draw()
        self.canvas.after(30, self.move)


    def start(self):
        self.f()
        self.move()
        self.died()


class tank1(tank):
    def __init__(self, canvas, points, color=TANK_COLOR1):
        tank.__init__(self, canvas, points, color)
        self.canvas.bind_all('<KeyPress-w>', self.press_forward)
        self.canvas.bind_all('<KeyRelease-w>', self.release_forward)
        self.canvas.bind_all('<KeyPress-a>', self.press_left)
        self.canvas.bind_all('<KeyRelease-a>', self.release_left)
        self.canvas.bind_all('<KeyPress-s>', self.press_backward)
        self.canvas.bind_all('<KeyRelease-s>', self.release_backward)
        self.canvas.bind_all('<KeyPress-d>', self.press_right)
        self.canvas.bind_all('<KeyRelease-d>', self.release_right)
        self.canvas.bind_all('<KeyPress-r>', self.press_fire)
        self.canvas.bind_all('<KeyRelease-r>', self.release_fire)


class tank2(tank):
    def __init__(self, canvas, points, color=TANK_COLOR2):
        tank.__init__(self, canvas, points, color)
        self.canvas.bind_all('<KeyPress-Up>', self.press_forward)
        self.canvas.bind_all('<KeyRelease-Up>', self.release_forward)
        self.canvas.bind_all('<KeyPress-Left>', self.press_left)
        self.canvas.bind_all('<KeyRelease-Left>', self.release_left)
        self.canvas.bind_all('<KeyPress-Down>', self.press_backward)
        self.canvas.bind_all('<KeyRelease-Down>', self.release_backward)
        self.canvas.bind_all('<KeyPress-Right>', self.press_right)
        self.canvas.bind_all('<KeyRelease-Right>', self.release_right)
        self.canvas.bind_all('<KeyPress-l>', self.press_fire)
        self.canvas.bind_all('<KeyRelease-l>', self.release_fire)