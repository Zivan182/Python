import math
import time
from wall import *
from bullet import *
from geometry import *
from constants import *


class Tank():
    """ Класс Tank - танк

    Attributes
    ----------
    points : list
        список вершин танка
    A,B,C,D : list
        вершины танка
    O : list
        центр танка
    muzzle : list
        "дуло" танка (место, откуда вылетает пуля)
    dx, dy : float
        смещение танка по осям Ox/Oy при движении
    color : str, optional
        цвет танка
    bullets : int
        количество выпущенных пуль в данный момент
    pressed : list
        список индикаторов нажатия клавиш
    stopped : bool
        индикатор движения танка

    Methods
    -------
    update()
        обновляет координаты вершин танка, координаты центра, координаты дула, значения dx и dy
    collision()
        проверяет столкновения танка со стенами
    shift(dx, dy)
        производит смещение танка на указанные величины dx и dy
    move_forward()
        производит движение танка вперед
    move_backward()
        производит движение танка назад
    rotate_left()
        производит поворот танка налево
    rotate_right()
        производит поворот танка направо
    delete_bullet()
        уменьшает количество выпущенных пуль на 1, когда пуля исчезает
    fire()
        производит выстрел, уничтожает пулю через 10s
    died()
        проверяет столкновения танка с пулей каждые 30ms;
        в случае столкновения игра заканчивается
    press_<...>()
        устанавливает индикатор того, что соответственная клавиша нажата
    release_<...>()
        устанавливает индикатор того, что соответственная клавиша не нажата
    f()
        запускает метод fire(), если нажата клавиша стрельбы;
        вызывает себя снова через 30ms
    move()
        запускает движение и поворот танка, если нажаты соответственные клавиши;
        производит отрисовку танка;
        вызывает себя снова через 30ms
    start()
        вызывается при создании танка;
        запускает методы f(), move(), died()
    """

    def __init__(self, canvas, points, color):
        self.canvas = canvas
        self.points = points
        self.update()
        self.color = color
        self.id = self.canvas.create_polygon(self.points, fill=color, outline=OUTLINE1)
        self.bullets = 0
        self.pressed = {'forward': False, 'left': False, 'backward': False, 'right': False, 'fire': False}
        self.stopped = False
        self.start()


    def update(self):
        """обновляет координаты вершин танка, координаты центра, координаты дула, значения dx и dy"""

        self.A, self.B, self.C, self.D = self.points
        self.O = [(self.A[0] + self.C[0]) / 2, (self.A[1] + self.C[1]) / 2]
        self.muzzle = [(self.A[0] + self.B[0]) / 2, (self.A[1] + self.B[1]) / 2]
        self.dx = (self.muzzle[0] - self.O[0]) * SMALL_CONSTANT
        self.dy = (self.muzzle[1] - self.O[1]) * SMALL_CONSTANT


    def collision(self):
        """проверяет столкновения танка со стенами"""

        for v_wall in vertical_walls:
            begin = [v_wall.x, v_wall.y]
            end = [v_wall.x, v_wall.y + v_wall.len]
            if intersect_of_segments(self.A, self.B, begin, end) or \
                    intersect_of_segments(self.B, self.C, begin, end) or \
                    intersect_of_segments(self.C, self.D, begin, end) or \
                    intersect_of_segments(self.D, self.A, begin, end):
                return v_wall
        for h_wall in horizontal_walls:
            begin = [h_wall.x, h_wall.y]
            end = [h_wall.x + h_wall.len, h_wall.y]
            if intersect_of_segments(self.A, self.B, begin, end) or \
                    intersect_of_segments(self.B, self.C, begin, end) or \
                    intersect_of_segments(self.C, self.D, begin, end) or \
                    intersect_of_segments(self.D, self.A, begin, end):
                return h_wall
        return False


    def shift(self, dx, dy):
        """производит смещение танка на указанные величины dx и dy

        Parameters
        ----------
        dx, dy : float
            смещение танка по оси Ox/Oy
        """

        for i in range(4):
            self.points[i][0] += dx
            self.points[i][1] += dy


    def move_forward(self):
        """производит движение танка вперед"""

        self.canvas.move(self.id, self.dx, self.dy)
        self.shift(self.dx, self.dy)
        self.update()


    def move_backward(self):
        """производит движение танка назад"""

        self.canvas.move(self.id, -self.dx, -self.dy)
        self.shift(-self.dx, -self.dy)
        self.update()


    def rotate_left(self, angle=ANGLE):
        """производит поворот танка налево

        Parameters
        ----------
        angle : float, optional
            угол поворота в радианах
        """

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
        """производит поворот танка направо

        Parameters
        ----------
        angle : float, optional
            угол поворота в радианах
        """

        s = math.sin(angle)
        c = math.cos(angle)
        self.canvas.create_polygon(self.points, fill=BG_COLOR, outline=BG_COLOR)
        for i in range(4):
            x, y = self.points[i]
            self.points[i][0] = self.O[0] + c * (x - self.O[0]) - s * (y - self.O[1])
            self.points[i][1] = self.O[1] + s * (x - self.O[0]) + c * (y - self.O[1])
        self.id = self.canvas.create_polygon(self.points, fill=self.color, outline=OUTLINE1)
        self.update()


    def delete_bullet(self):
        """уменьшает количество выпущенных пуль на 1, когда пуля исчезает"""

        self.bullets -= 1


    def fire(self):
        """производит выстрел, уничтожает пулю через 10s"""

        if self.bullets < 5:
            tank_bullet = Bullet(self.canvas, self.muzzle[0] + STEP * self.dx, self.muzzle[1] + STEP * self.dy,
                                 2 * self.dx, 2 * self.dy)
            self.bullets += 1
            bullets.append(tank_bullet)
            self.canvas.after(10000, self.delete_bullet)


    def died(self):
        """проверяет столкновения танка с пулей каждые 30ms;
        в случае столкновения игра заканчивается
        """

        for bull in bullets:
            if distance(self.O[0], self.O[1], bull.x, bull.y) <= bull.r + 15:
                time.sleep(3)
                self.canvas.quit()
        self.canvas.after(30, self.died)


    def press_forward(self, event):
        """устанавливает индикатор того, что клавиша движения вперед нажата"""

        self.pressed['forward'] = True


    def release_forward(self, event):
        """устанавливает индикатор того, что клавиша движения вперед не нажата"""

        self.pressed['forward'] = False


    def press_left(self, event):
        """устанавливает индикатор того, что клавиша поворота влево нажата"""

        self.pressed['left'] = True


    def release_left(self, event):
        """устанавливает индикатор того, что клавиша поворота влево не нажата"""

        self.pressed['left'] = False


    def press_backward(self, event):
        """устанавливает индикатор того, что клавиша движения назад нажата"""

        self.pressed['backward'] = True


    def release_backward(self, event):
        """устанавливает индикатор того, что клавиша движения назад не нажата"""

        self.pressed['backward'] = False


    def press_right(self, event):
        """устанавливает индикатор того, что клавиша поворота вправо нажата"""

        self.pressed['right'] = True


    def release_right(self, event):
        """устанавливает индикатор того, что клавиша поворота вправо не нажата"""

        self.pressed['right'] = False


    def press_fire(self, event):
        """устанавливает индикатор того, что клавиша стрельбы нажата"""

        self.pressed['fire'] = True


    def release_fire(self, event):
        """устанавливает индикатор того, что клавиша стрельбы не нажата"""

        self.pressed['fire'] = False


    def f(self):
        """запускает метод fire(), если нажата клавиша стрельбы;
        вызывает себя снова через 30ms
        """

        if (self.pressed['fire']):
            self.fire()
        self.canvas.after(200, self.f)


    def move(self):
        """запускает движение и поворот танка, если нажаты соответственные клавиши;
        производит отрисовку танка;
        вызывает себя снова через 30ms
        """

        if not self.stopped:
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
        """вызывается при создании танка;
        запускает методы f(), move(), died()
        """

        self.f()
        self.move()
        self.died()


class Tank1(Tank):
    """Класс Tank1 - первый танк
    наследуется от класса Tank

    Управление
    ----------
    'W' - движение вперед
    'A' - поворот налево
    'S' - движение назад
    'D' - поворот направо
    'R' - стрельба
    """

    def __init__(self, canvas, points, color=TANK_COLOR1):
        Tank.__init__(self, canvas, points, color)
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


class Tank2(Tank):
    """Класс Tank2 - второй танк
    наследуется от класса Tank

    Управление
    ----------
    'Up' - движение вперед
    'Left' - поворот налево
    'Down' - движение назад
    'Right' - поворот направо
    'L' - стрельба
    """

    def __init__(self, canvas, points, color=TANK_COLOR2):
        Tank.__init__(self, canvas, points, color)
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
