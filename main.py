from tkinter import *
import time
from random import randint
import math
from tank import *
from wall import *
from bullet import *
from generate_maze import *
from draw_maze import *
from geometry import *
from variables import *

root = Tk()
root.geometry("1200x600+30+20")
root.title("Танки в лабиринте")
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
canvas.pack()
canvas.quit()
root.update()

def main():
    up = HorizontalWall(canvas, 0, 0, WIDTH)
    down = HorizontalWall(canvas, 0, HEIGHT, WIDTH)
    left = VerticalWall(canvas, 0, 0, HEIGHT)
    right = VerticalWall(canvas, WIDTH, 0, HEIGHT)
    vertical_walls.append(left)
    vertical_walls.append(right)
    horizontal_walls.append(up)
    horizontal_walls.append(down)
    draw_maze(canvas)
    tank_second = Tank2(canvas, [[1175,565],[1195,565],[1195,595],[1175,595]])
    tank_first = Tank1(canvas, [[25,35], [5,35], [5,5], [25,5]])
    tank_first.start()
    tank_second.start()
    root.update_idletasks()
    root.update()
    time.sleep(0.01)
    root.mainloop()

if __name__=='__main__':
    main()
