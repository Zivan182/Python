from random import *
from variables import *


def maze_generator(n,m):
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