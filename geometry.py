import math

class Vector():
    """Класс Vector - вектор

    Attributes
    ----------
    x, y : float
        координаты вектора

    Methods
    -------
    @staticmethod
    multiply(v, k)
        умножение вектора v на число k

    @staticmethod
    v_multiply(v1, v2)
        векторное произведение векторов v1 и v2

    @staticmethod
    diff(v1, v2)
        разность векторов v1 и v2

    @staticmethod
    summ(v1, v2)
        сумма векторов v1 и v2
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def multiply(v, k):
        """умножение вектора на число

        Parameters
        ----------
        v : Vector
            вектор
        k : float
            число
        """

        v.x *= k
        v.y *= k
        return v

    @staticmethod
    def v_multiply(v1, v2):
        """векторное произведение

        Parameters
        ----------
        v1, v2 : Vector
            векторы
        """

        return v1.x * v2.y - v1.y * v2.x

    @staticmethod
    def diff(v1, v2):
        """разность векторов

        Parameters
        ----------
        v1, v2 : Vector
            векторы
        """

        return Vector(v1.x - v2.x, v1.y - v2.y)

    @staticmethod
    def summ(v1, v2):
        """сумма векторов

        Parameters
        ----------
        v1, v2 : Vector
            векторы
        """

        return Vector(v1.x + v2.x, v1.y + v2.y)


class Line():
    """Класс Line - прямая

    Attributes
    ----------
    rds : Vector
        радиус-вектор
    drct : Vector
        направляющий вектор

    Methods
    -------
    @staticmethod
    intersect1(l1, l2)
        пересечение прямых l1 и l2

    @staticmethod
    intersect(a, b, c, d)
        пересечение прямых ab и cd
    """

    def __init__(self, rds, drct):
        self.rds = rds
        self.drct = drct

    @staticmethod
    def intersect1(l1, l2):
        """пересечение прямых

        Parameters
        ----------
        l1, l2 : Line
            прямые
        """

        if Vector.v_multiply(l1.drct, l2.drct) == 0:
            return Vector(2000, 2000)
        t = Vector.v_multiply(l2.drct, Vector.diff(l1.rds, l2.rds)) / Vector.v_multiply(l1.drct, l2.drct)
        return Vector.summ(l1.rds, Vector.multiply(l1.drct, t))

    @staticmethod
    def intersect(a, b, c, d):
        """пересечение прямых

        Parameters
        ----------
        a, b : list
            точки на первой прямой
        c, d : list
            точки на второй прямой
        """

        l1 = Line(Vector(a[0], a[1]), Vector(a[0] - b[0], a[1] - b[1]))
        l2 = Line(Vector(c[0], c[1]), Vector(c[0] - d[0], c[1] - d[1]))
        ans = Line.intersect1(l1, l2)
        return [ans.x, ans.y]


def intersect_of_segments(a, b, c, d):
    """индикатор пересечения отрезков

    Parameters
    ----------
    a, b : list
        вершины первого отрезка
    c, d : list
        вершины второго отрезка
    """

    x, y = Line.intersect(a, b, c, d)
    if ((a[0] - x) * (b[0] - x) <= 0 and (a[1] - y) * (b[1] - y) <= 0) \
            and ((c[0] - x) * (d[0] - x) <= 0 and (c[1] - y) * (d[1] - y) <= 0):
        return True
    return False


def distance(x1, y1, x2, y2):
    """расстояние между точками

    Parameters
    ----------
    x1, y1 : float
        координаты первой точки
    x2, y2 : float
        координаты второй точки
    """

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


