from maze_generator import *
from wall import *
from variables import *


def maze_drawer(canvas):
    maze_walls = maze_generator(N, M)
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