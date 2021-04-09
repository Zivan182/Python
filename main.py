from tkinter import *

import time
import random
from random import randint
import math

from tank import *
from wall import *
from bullet import *
from maze_generator import *
from maze_drawer import *
from geometry import *
from variables import *




root = Tk()
root.geometry("1200x600+30+20")
root.title("Танки в лабиринте")

canvas = Canvas(root, width = WIDTH, height = HEIGHT, bg = BG_COLOR)
canvas.pack()
canvas.quit()
root.update()

up = horizontal_wall(canvas, 0, 0, WIDTH)
down = horizontal_wall(canvas, 0, HEIGHT, WIDTH)
left = vertical_wall(canvas, 0, 0, HEIGHT)
right = vertical_wall(canvas, WIDTH, 0, HEIGHT)

vertical_walls.append(left)
vertical_walls.append(right)
horizontal_walls.append(up)
horizontal_walls.append(down)

maze_drawer(canvas)
tank_second = tank2(canvas, [[1175,565],[1195,565],[1195,595],[1175,595]])
tank_first = tank1(canvas, [[25,35], [5,35], [5,5], [25,5]])

tank_first.start()
tank_second.start()

#quitButton = Button(root, text="Закрыть окно", command=root.quit)
#quitButton.place(x=0, y=0)
#quitButton.pack(expand = True, fill = BOTH)
#canvas.create_text(10, 10, text='1234', font=('Courier', 15), fill='black')

root.update_idletasks()
root.update()
time.sleep(0.01)
root.mainloop()







