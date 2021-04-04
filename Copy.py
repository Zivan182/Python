from tkinter import *

import time
import random
from random import randint
import math

WIDTH = 1200
HEIGHT = 600
BG_COLOR = 'white'
SMALL_CONSTANT = 0.2
BULLET_R = 5
BULLET_COLOR = 'black'
WALL_COLOR = 'grey'
TANK_COLOR = 'red'
TANK_COLOR2 = 'green'
WALL_LEN = 60
STEP = 1.2
ANGLE = 0.1
N = 10
M = 20



root = Tk()
root.title("Танки в лабиринте")


canvas = Canvas(root, width = WIDTH, height = HEIGHT, bg = BG_COLOR)
canvas.pack()
root.update()


class vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
def multiply(vector, k):
    vector.x *= k
    vector.y *= k
    return vector
def v_multiply(v1, v2):
    return v1.x * v2.y - v1.y * v2.x
def diff(v1, v2):
    return vector(v1.x - v2.x, v1.y - v2.y)
def summ(v1, v2):
    return vector(v1.x + v2.x, v1.y + v2.y)
class line():
    def __init__(self, rds, drct):
        self.rds = rds
        self.drct = drct
def intersect(l1, l2):
    t = v_multiply(l2.drct, diff(l1.rds, l2.rds)) / v_multiply(l1.drct, l2.drct)
    return summ(l1.rds, multiply(l1.drct, t))
def per(v, l):
    direct = vector(-l.drct.y, l.drct.x)
    return line(v, direct)
def projection(v, l):
    perpendikular = per(v, l)
    return intersect(perpendikular, line)
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
def distance1(v1, v2):
    return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)
def distance2(v, l):
    return distance1(v, projection(v, l))



class vertical_wall():
    def __init__(self, canvas, x, y, len = WALL_LEN, color = WALL_COLOR):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.len = len
        self.color = color
        self.id = canvas.create_line(self.x, self.y, self.x, self.y + self.len)

    def draw(self):
        canvas.create_line(self.x, self.y, self.x, self.y + self.len)


class horizontal_wall():
    def __init__(self, canvas, x, y, len = WALL_LEN, color = WALL_COLOR):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.len = len
        self.color = color
        self.id = canvas.create_line(self.x, self.y, self.x + self.len, self.y)

    def draw(self):
        canvas.create_line(self.x, self.y, self.x + self.len, self.y)



class bullet():
    def __init__(self, canvas, x, y, dx, dy, r = BULLET_R, color = BULLET_COLOR):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = 'blue')

    def collision(self):
        if (self.x + self.r >= WIDTH) or (self.x - self.r <= 0):
            self.dx = -self.dx
        if (self.y + self.r >= HEIGHT) or (self.y - self.r <= 0):
            self.dy = -self.dy

        for v_wall in vertical_walls:
            if (v_wall.x - self.r <= self.x <= v_wall.x + self.r) and (v_wall.y <= self.y <= v_wall.y + v_wall.len):
                self.dx = -self.dx
                v_wall.draw()
            elif distance(self.x, self.y, v_wall.x, v_wall.y) <= self.r:
                self.dy = -self.dy
                v_wall.draw()
            elif distance(self.x, self.y, v_wall.x, v_wall.y + v_wall.len) <= self.r:
                self.dy = -self.dy
                v_wall.draw()

        for h_wall in horizontal_walls:
            if (h_wall.y - self.r <= self.y <= h_wall.y + self.r) and (h_wall.x <= self.x <= h_wall.x + h_wall.len):
                self.dy = -self.dy
                h_wall.draw()
            elif distance(self.x, self.y, v_wall.x, v_wall.y) <= self.r:
                self.dx = -self.dx
                h_wall.draw()
            elif distance(self.x, self.y, h_wall.x + h_wall.len, h_wall.y) <= self.r:
                self.dx = -self.dx
                h_wall.draw()



    def bullet_move(self):
        self.canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        self.collision()

        self.canvas.after(20, self.bullet_move)

    def bullet_delete(self):
        self.canvas.delete(self)







class tank1():
    def __init__(self, canvas, points, color = TANK_COLOR):
        self.canvas = canvas
        self.points = points
        self.A = points[0]
        self.B = points[1]
        self.C = points[2]
        self.D = points[3]
        self.O = [(self.A[0] + self.C[0]) / 2, (self.A[1] + self.C[1]) / 2]
        self.muzzle = [(self.A[0] + self.B[0]) / 2, (self.A[1] + self.B[1]) / 2]
        self.color = color
        self.dx = (self.muzzle[0] - self.O[0]) * SMALL_CONSTANT
        self.dy = (self.muzzle[1] - self.O[1]) * SMALL_CONSTANT

        self.id = canvas.create_polygon(self.points, fill = TANK_COLOR)
        self.bullets = 0

        self.pressed = {'w':False,'a':False,'s':False, 'd':False, 'r':False}

        self.canvas.bind_all('<KeyPress-w>', self.press_w)
        self.canvas.bind_all('<KeyRelease-w>', self.release_w)
        self.canvas.bind_all('<KeyPress-a>', self.press_a)
        self.canvas.bind_all('<KeyRelease-a>', self.release_a)
        self.canvas.bind_all('<KeyPress-s>', self.press_s)
        self.canvas.bind_all('<KeyRelease-s>', self.release_s)
        self.canvas.bind_all('<KeyPress-d>', self.press_d)
        self.canvas.bind_all('<KeyRelease-d>', self.release_d)
        self.canvas.bind_all('<KeyPress-r>', self.press_r)
        self.canvas.bind_all('<KeyRelease-r>', self.release_r)


    def draw(self):
        canvas.create_polygon(self.points, fill=TANK_COLOR)


    def update(self):
        self.A = self.points[0]
        self.B = self.points[1]
        self.C = self.points[2]
        self.D = self.points[3]
        self.O = [(self.A[0] + self.C[0]) / 2, (self.A[1] + self.C[1]) / 2]
        self.muzzle = [(self.A[0] + self.B[0]) / 2, (self.A[1] + self.B[1]) / 2]
        self.dx = (self.muzzle[0] - self.O[0]) * SMALL_CONSTANT
        self.dy = (self.muzzle[1] - self.O[1]) * SMALL_CONSTANT


    def move_forward(self):
        canvas.create_polygon(self.points, fill=BG_COLOR)
        new_points = []
        for x,y in self.points:
            new_x = x + self.dx
            new_y = y + self.dy
            new_points.append([new_x, new_y])
        self.points = new_points
        self.id = canvas.create_polygon(self.points, fill=TANK_COLOR)
        self.update()
        print(self.A[0], self.O[1])

    def move_backward(self):
        canvas.create_polygon(self.points, fill=BG_COLOR)
        new_points = []
        for x, y in self.points:
            new_x = x - self.dx
            new_y = y - self.dy
            new_points.append([new_x, new_y])
        self.points = new_points
        self.id = canvas.create_polygon(self.points, fill=TANK_COLOR)
        self.update()
        print(self.O[0], self.O[1])

    def rotate_left(self, angle = ANGLE):
        s = math.sin(angle)
        c = math.cos(angle)
        new_points = []
        canvas.create_polygon(self.points, fill=BG_COLOR)
        for x, y in self.points:
            new_x = self.O[0] + c * (x - self.O[0]) + s * (y - self.O[1])
            new_y = self.O[1] - s * (x - self.O[0]) + c * (y - self.O[1])
            new_points.append([new_x, new_y])
        self.points = new_points
        self.id = canvas.create_polygon(self.points, fill=TANK_COLOR)
        self.update()
        print(self.O[0], self.O[1])

    def rotate_right(self, angle = ANGLE):
        s = math.sin(angle)
        c = math.cos(angle)
        new_points = []
        canvas.create_polygon(self.points, fill=BG_COLOR)
        for x,y in self.points:
            new_x = self.O[0] + c * (x - self.O[0]) - s * (y - self.O[1])
            new_y = self.O[1] + s * (x - self.O[0]) + c * (y - self.O[1])
            new_points.append([new_x,new_y])
        self.points = new_points
        self.id = canvas.create_polygon(self.points, fill=TANK_COLOR)
        self.update()
        print(self.O[0], self.O[1])

    def fire(self):
        if self.bullets < 5:
            tank_bullet = bullet(canvas, self.muzzle[0] + STEP * self.dx, self.muzzle[1] + STEP * self.dy, 2 * self.dx, 2 * self.dy)
            self.bullets += 1
            bullets.append(tank_bullet)
            tank_bullet.bullet_move()
            self.canvas.after(30, lambda: tank_bullet.delete())








    def press_w(self, event):
        self.pressed['w'] = True
        #print(12)
    def release_w(self, event):
        self.pressed['w'] = False
        #print(13)


    def press_a(self, event):
        self.pressed['a'] = True
    def release_a(self, event):
        self.pressed['a'] = False


    def press_s(self, event):
        self.pressed['s'] = True
    def release_s(self, event):
        self.pressed['s'] = False


    def press_d(self, event):
        self.pressed['d'] = True
    def release_d(self, event):
        self.pressed['d'] = False


    def press_r(self, event):
        self.pressed['r'] = True
    def release_r(self, event):
        self.pressed['r'] = False

    def f(self):
        if (self.pressed['r']):
            self.fire()
        self.canvas.after(200, self.f)

    def ost(self):
        if (self.pressed['w']):
            self.move_forward()
        if (self.pressed['s']):
            self.move_backward()
        if (self.pressed['a']):
            self.rotate_left()
        if (self.pressed['d']):
            self.rotate_right()
        self.draw()

        self.canvas.after(30, self.ost)





    def move(self):
        self.f()
        self.ost()


class tank2():
    def __init__(self, canvas, points, color = TANK_COLOR2):
        self.canvas = canvas
        self.points = points
        self.A = points[0]
        self.B = points[1]
        self.C = points[2]
        self.D = points[3]
        self.O = [(self.A[0] + self.C[0]) / 2, (self.A[1] + self.C[1]) / 2]
        self.muzzle = [(self.A[0] + self.B[0]) / 2, (self.A[1] + self.B[1]) / 2]
        self.color = color
        self.dx = (self.muzzle[0] - self.O[0]) * SMALL_CONSTANT
        self.dy = (self.muzzle[1] - self.O[1]) * SMALL_CONSTANT

        self.id = canvas.create_polygon(self.points, fill = TANK_COLOR2)
        self.bullets = 0

        self.pressed = {'Up':False,'Left':False,'Down':False, 'Right':False, 'l':False}

        self.canvas.bind_all('<KeyPress-Up>', self.press_Up)
        self.canvas.bind_all('<KeyRelease-Up>', self.release_Up)
        self.canvas.bind_all('<KeyPress-Left>', self.press_Left)
        self.canvas.bind_all('<KeyRelease-Left>', self.release_Left)
        self.canvas.bind_all('<KeyPress-Down>', self.press_Down)
        self.canvas.bind_all('<KeyRelease-Down>', self.release_Down)
        self.canvas.bind_all('<KeyPress-Right>', self.press_Right)
        self.canvas.bind_all('<KeyRelease-Right>', self.release_Right)
        self.canvas.bind_all('<KeyPress-l>', self.press_Space)
        self.canvas.bind_all('<KeyRelease-l>', self.release_Space)


    def draw(self):
        canvas.create_polygon(self.points, fill=TANK_COLOR2)


    def update(self):
        self.A = self.points[0]
        self.B = self.points[1]
        self.C = self.points[2]
        self.D = self.points[3]
        self.O = [(self.A[0] + self.C[0]) / 2, (self.A[1] + self.C[1]) / 2]
        self.muzzle = [(self.A[0] + self.B[0]) / 2, (self.A[1] + self.B[1]) / 2]
        self.dx = (self.muzzle[0] - self.O[0]) * SMALL_CONSTANT
        self.dy = (self.muzzle[1] - self.O[1]) * SMALL_CONSTANT


    def move_forward(self):
        canvas.create_polygon(self.points, fill=BG_COLOR)
        new_points = []
        for x,y in self.points:
            new_x = x + self.dx
            new_y = y + self.dy
            new_points.append([new_x, new_y])
        self.points = new_points
        self.id = canvas.create_polygon(self.points, fill=TANK_COLOR2)
        self.update()
        print(self.A[0], self.O[1])

    def move_backward(self):
        canvas.create_polygon(self.points, fill=BG_COLOR)
        new_points = []
        for x, y in self.points:
            new_x = x - self.dx
            new_y = y - self.dy
            new_points.append([new_x, new_y])
        self.points = new_points
        self.id = canvas.create_polygon(self.points, fill=TANK_COLOR2)
        self.update()
        print(self.O[0], self.O[1])

    def rotate_left(self, angle = ANGLE):
        s = math.sin(angle)
        c = math.cos(angle)
        new_points = []
        canvas.create_polygon(self.points, fill=BG_COLOR)
        for x, y in self.points:
            new_x = self.O[0] + c * (x - self.O[0]) + s * (y - self.O[1])
            new_y = self.O[1] - s * (x - self.O[0]) + c * (y - self.O[1])
            new_points.append([new_x, new_y])
        self.points = new_points
        self.id = canvas.create_polygon(self.points, fill=TANK_COLOR2)
        self.update()
        print(self.O[0], self.O[1])

    def rotate_right(self, angle = ANGLE):
        s = math.sin(angle)
        c = math.cos(angle)
        new_points = []
        canvas.create_polygon(self.points, fill=BG_COLOR)
        for x,y in self.points:
            new_x = self.O[0] + c * (x - self.O[0]) - s * (y - self.O[1])
            new_y = self.O[1] + s * (x - self.O[0]) + c * (y - self.O[1])
            new_points.append([new_x,new_y])
        self.points = new_points
        self.id = canvas.create_polygon(self.points, fill=TANK_COLOR2)
        self.update()
        print(self.O[0], self.O[1])

    def fire(self):
        if self.bullets < 5:
            tank_bullet = bullet(canvas, self.muzzle[0] + STEP * self.dx, self.muzzle[1] + STEP * self.dy, 2 * self.dx, 2 * self.dy)
            self.bullets += 1
            bullets.append(tank_bullet)
            tank_bullet.bullet_move()







    def press_Up(self, event):
        self.pressed['Up'] = True
    def release_Up(self, event):
        self.pressed['Up'] = False


    def press_Left(self, event):
        self.pressed['Left'] = True
    def release_Left(self, event):
        self.pressed['Left'] = False


    def press_Down(self, event):
        self.pressed['Down'] = True
    def release_Down(self, event):
        self.pressed['Down'] = False


    def press_Right(self, event):
        self.pressed['Right'] = True
    def release_Right(self, event):
        self.pressed['Right'] = False


    def press_Space(self, event):
        self.pressed['l'] = True
    def release_Space(self, event):
        self.pressed['l'] = False

    def f(self):
        if (self.pressed['l']):
            self.fire()
        self.canvas.after(200, self.f)

    def ost(self):
        if (self.pressed['Up']):
            self.move_forward()
        if (self.pressed['Down']):
            self.move_backward()
        if (self.pressed['Left']):
            self.rotate_left()
        if (self.pressed['Right']):
            self.rotate_right()
        self.draw()

        self.canvas.after(30, self.ost)

    def move(self):
        self.f()
        self.ost()



def maze(n,m):

    field = [[0 for i in range(m)] for i in range(n)]
    walls = [[[False, False] for i in range(m)] for i in range(n)]

    for i in range(n):
        a = dict()
        b = dict()
        field[i] = [s for s in range(i * m, (i + 1) * m)]
        if i > 0:
            for j in range(m):
                if walls[i][j][1] is False:
                    field[i][j] = field[i - 1][j]

        for j in range(1, m):
            if randint(0, 1) == 0:
                walls[i][j][0] = True
            else:
                field[i][j] = field[i][j - 1]
                a[field[i][j]] = a.get(field[i][j], 1) + 1
        if i < n - 1:
            for k in range(m):
                if (randint(0, 1) == 0) and (a.get(field[i][k], 0) - b.get(field[i][k], 0) > 1):
                    walls[i + 1][k][1] = True
                    b[field[i][k]] = b.get(field[i][k], 0) + 1
        if i == n - 1:
            s = 1
            while (s < m):
                if walls[i][s][0] and field[i][s - 1] != field[i][s]:
                    walls[i][s][0] = False
                    x = field[i][s]
                    while s < m and field[i][s] == x:
                        field[i][s] = field[i][s - 1]
                        s += 1
                else:
                    s += 1
    return walls

def create_maze():

    maze_walls = maze(N, M)
    #maze_walls = [[[False, False], [False, False], [False, False], [False, False]],[[False, True], [False, True], [False, True], [False, False]],[[False, False], [False, False], [True, False], [False, False]],[[False, True], [True, False], [True, False], [False, False]]             ]
    #print(maze_walls)

    for i in range(N):
        j = 1
        begin = 0
        number = 1
        while j<=M:
            if maze_walls[i][j - 1][1] is True and (j == M or maze_walls[i][j][1] is False):
                horizontal_walls.append(horizontal_wall(canvas, 60 * begin, 60 * i, 60 * number))
                number = 1
            if j<M and maze_walls[i][j][1] is True and maze_walls[i][j - 1][1] is True:
                number += 1
            if j<M and maze_walls[i][j][1] is True and maze_walls[i][j - 1][1] is False:
                begin = j
            j += 1

    for j in range(M):
        i = 1
        begin = 0
        number = 1
        while i<=N:
            if maze_walls[i - 1][j][0] is True and (i == N or maze_walls[i][j][0] is False):
                vertical_walls.append(vertical_wall(canvas, 60 * j, 60 * begin, 60 * number))
                number = 1
            if i<N and maze_walls[i][j][0] is True and maze_walls[i - 1][j][0] is True:
                number += 1
            if i<N and maze_walls[i][j][0] is True and maze_walls[i - 1][j][0] is False:
                begin = i
            i += 1



def start_walls():
    for v_wall in vertical_walls:
        v_wall.draw()
    for h_wall in horizontal_walls:
        h_wall.draw()
#canvas.after(100, start_walls)
def start_tanks():
    for tank in tanks:
        tank.move()
    #canvas.after(30, start_tanks)
def start_bullets():
    for bullet in bullets:
        bullet.bullet_move()
    canvas.after(40, start_bullets)






vertical_walls = []
horizontal_walls = []
bullets = []
tanks = []
create_maze()
tank_second = tank2(canvas, [[1180,570],[1200,570],[1200,600],[1180,600]])
tank_first = tank1(canvas, [[20,30], [0,30], [0,0], [20,0]])



#vertical_wall(canvas, 5, 60)
tanks.append(tank_first)
tanks.append(tank_second)
#start_walls()
start_tanks()
#start_bullets()




root.update_idletasks()

root.update()

time.sleep(0.01)

root.mainloop()




