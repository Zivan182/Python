import math

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


def intersect1(l1, l2):
    if v_multiply(l1.drct, l2.drct) == 0:
        return vector(2000, 2000)
    t = v_multiply(l2.drct, diff(l1.rds, l2.rds)) / v_multiply(l1.drct, l2.drct)
    return summ(l1.rds, multiply(l1.drct, t))


def intersect(a, b, c, d):
    l1 = line(vector(a[0], a[1]), vector(a[0] - b[0], a[1] - b[1]))
    l2 = line(vector(c[0], c[1]), vector(c[0] - d[0], c[1] - d[1]))
    ans = intersect1(l1,l2)
    return [ans.x, ans.y]


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def intersect_of_segments(a, b, c, d):
    x, y = intersect(a, b, c, d)
    if ((a[0] - x) * (b[0] - x) <=0 and (a[1] - y) * (b[1] - y) <= 0) \
            and ((c[0] - x) * (d[0] - x) <= 0 and (c[1] - y) * (d[1] - y) <=0):
        return True
    return False
