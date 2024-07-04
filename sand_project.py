from tkinter import Tk, Canvas, ttk
from math import floor, ceil
from random import choice, seed
from datetime import datetime

# Set randomness for mounds
seed(datetime.now().timestamp())

# TODO: SHOW VALUES OF SLIDERS (START AND END VALUES)
# TODO: MAKE IT LOOK NICE

# Initial parameters
h = 600
w = 900
# Default at 3
size = 3
g = 0.006
colour = 'blue'

collision = (w // size) * [h]

class Particle:
    def __init__(self, x0, y0, x1, y1, space):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.dt = 1
        self.space = space
        self.particle = space.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=str(colour_choose.get().lower()), outline=str(colour_choose.get().lower()))
    
    def move_particle(self, dt=51):
        # Changeable from oustide
        self.dt += (g_slider.get() * g)

        # Non changeable from outside
        dx = 0
        dy = size
        index = self.x0 // size

        # Moves Particle if not directly underneath another
        if (self.y1 + dy < collision[index] - (size-1)):     
            self.space.after(ceil(50 / self.dt), self.move_particle)
            self.space.move(self.particle, dx, dy)
            self.x0 += dx
            self.y0 += dy
            self.x1 += dx
            self.y1 += dy
        # Special case (right edge)
        elif (w - size == self.x0):
            # Leftward movement under special case (right edge initial placement)
            if (collision[(self.x0 - size) // size] - size >= self.y1 + size - 1) and (self.x0 >= size):
                dx = -1 * size
                self.space.after(ceil(70 / self.dt), self.move_particle)
                self.space.move(self.particle, dx, dy)
                self.x0 += dx
                self.y0 += dy
                self.x1 += dx
                self.y1 += dy
            else:
                dx = size
                self.space.after(0, self.space.move(self.particle, 0, collision[index] - self.y1))
                self.update_collision_map()
        # If both free, introduce randomness
        elif (collision[(self.x0 - size) // size] - size > self.y1 + size - 1) and (collision[(self.x0 + size) // size] - size > self.y1 + size - 1):
            dx = choice([-1, 1]) * size
            self.space.after(ceil(70 / self.dt), self.move_particle)
            self.space.move(self.particle, dx, dy)
            self.x0 += dx
            self.y0 += dy
            self.x1 += dx
            self.y1 += dy
        # If bottom left is free
        elif (collision[(self.x0 - size) // size] - size >= self.y1 + size - 1) and (self.x0 >= size):
            dx = -1 * size
            self.space.after(ceil(70 / self.dt), self.move_particle)
            self.space.move(self.particle, dx, dy)
            self.x0 += dx
            self.y0 += dy
            self.x1 += dx
            self.y1 += dy
        # If bottom right is free
        elif (collision[(self.x0 + size) // size] - size > self.y1 + size - 1) and (self.x0 <= w - size):
            dx = size
            self.space.after(ceil(70 / self.dt), self.move_particle)
            self.space.move(self.particle, dx, dy)
            self.x0 += dx
            self.y0 += dy
            self.x1 += dx
            self.y1 += dy
        # Considers possible distance for last "move" between collision and particle
        else:
            self.space.after(0, self.space.move(self.particle, dx, collision[index] - self.y1))
            self.update_collision_map()
            # Delete object: object's other instances of recursion removed
            del self

    def add_particle(event):
        # Frequency of particle adding
        space.after(20-int(freq_slider.get()))
        # Finds nearest block to add particle depending on size
        x = size*floor(event.x / size) if (event.x % 1 < 0.5) else size*ceil(event.x / size)
        y = size*floor(event.y / size) if (event.y % 1 >= 0.5) else size*ceil(event.y / size)
        # Only adds particle if above collision mapd
        index = x // size
        if (x < w-1) and (y < collision[index]):
            new_particle = Particle(x, y, x+size, y+size, space)
            new_particle.move_particle(50)

    def update_collision_map(self):
        # Need to get x coord, find last block placed
        index = self.x0 // size
        collision[index] -= size if (collision[index] > 0) else 0


# TODO: Get realtime value of scale


# Basic TK
root = Tk()
root.title("Sandbox")
root.geometry("1234x630")
root.resizable(False, False)
space = Canvas(root, bg="black", height=h+5, width=w)
space.create_line(0, h, w+10, h, fill="white", width=4)
space.grid(row = 0, column = 0, rowspan = 9, padx = 10, pady = 10)

# Adding particles with hold and click
space.bind("<B1-Motion>", Particle.add_particle)
space.bind("<Button-1>", Particle.add_particle)

# Settings Title
settings_title = ttk.Label(root, text="Experimental Settings")
settings_title.grid(row = 2, column=2, columnspan=2)
settings_title.configure(font=("Consolas", 15, "bold"))

# NOTE: Gravity Slider [SHOW VALUE AS UPDATES]
g_slider = ttk.Scale(root, from_ = 0, to = 30, orient = "horizontal")
g_slider.set(15)
g_label = ttk.Label(root, text="Gravity")

g_label.grid(row = 3, column = 2, padx = 10)
g_slider.grid(row = 3, column = 3)
g_label.configure(font=("Consolas", 10, "bold"))


# NOTE: Particle Frequency Slider [SHOW VALUE AS UPDATES]
freq_slider = ttk.Scale(root, from_ = 0, to = 20, orient = "horizontal")
freq_slider.set(10)
freq_label = ttk.Label(root, text="Particle Frequency")
freq_label.grid(row = 4, column = 2, padx = 10)
freq_slider.grid(row = 4, column = 3, padx = 5)
freq_label.configure(font=("Consolas", 10, "bold"))

# Colour Selection for particles
options = ["Blue", "Red", "Orange", "Yellow", "Green", "Pink", "Purple", "White"]
colour_choose = ttk.Combobox(root, values = options)
colour_choose.current(0)
colour_choose.grid(row = 5, column = 3, padx = 2)
colour_label = ttk.Label(root, text="Particle Colour")
colour_label.grid(row = 5, column = 2, padx = 2)
colour_label.configure(font=("Consolas", 10, "bold"))

# Run
root.mainloop()
