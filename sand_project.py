from tkinter import Tk, Canvas, ttk, Button
from math import floor, ceil
from random import choice, seed
from datetime import datetime

# Set randomness for dunes if no slope
seed(datetime.now().timestamp())

# Initial parameters
h = 600
w = 900
# Default at 9 (can change), default gravity, default colour
size = 9
g = 0.005
colour = 'blue'

# Initialising Collision Map
collision = (w // size) * [h]

# List of all particles (used for removal/reset)
particle_list = []

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
        # Gravity change (Changeable from oustide of class)
        self.dt += (g_slider.get() * g)

        # Change in position and current particle position (Non changeable from outside of class)
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
        # If both free, introduce randomness (slope both ways)
        elif (collision[(self.x0 - size) // size] - size > self.y1 + size - 1) and (collision[(self.x0 + size) // size] - size > self.y1 + size - 1):
            dx = choice([-1, 1]) * size
            self.space.after(ceil(70 / self.dt), self.move_particle)
            self.space.move(self.particle, dx, dy)
            self.x0 += dx
            self.y0 += dy
            self.x1 += dx
            self.y1 += dy
        # If bottom left is free (slope left)
        elif (collision[(self.x0 - size) // size] - size >= self.y1 + size - 1) and (self.x0 >= size):
            dx = -1 * size
            self.space.after(ceil(70 / self.dt), self.move_particle)
            self.space.move(self.particle, dx, dy)
            self.x0 += dx
            self.y0 += dy
            self.x1 += dx
            self.y1 += dy
        # If bottom right is free (slope right)
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
        # Finds nearest space to add particle depending on size
        x = size*floor(event.x / size) if (event.x % 1 < 0.5) else size*ceil(event.x / size)
        y = size*floor(event.y / size) if (event.y % 1 >= 0.5) else size*ceil(event.y / size)
        # Only adds particle if above collision map (not below dunes)
        index = x // size
        if (x < w-1) and (y < collision[index]):
            new_particle = Particle(x, y, x+size, y+size, space)
            new_particle.move_particle(50)
            particle_list.append(new_particle)

    def update_collision_map(self):
        # For where block needs to stop due to sand dune
        index = self.x0 // size
        collision[index] -= size if (collision[index] > 0) else 0

    def reset():
        # Clears canvas
        space.delete("all")
        # Redraws base line
        space.create_line(0, h, w+10, h, fill="white", width=4)
        # Resets collision map and deletes all particles objects
        for i in range(len(collision)):
            collision[i] = h
        for particle in particle_list:
            del particle


# Basic TK (Window not resizable)
root = Tk()
root.title("Sandbox")
root.geometry("1248x630")
root.resizable(False, False)

# Creates space where particles will fall until stopped by a white line
space = Canvas(root, bg="black", height=h+5, width=w)
space.create_line(0, h, w+10, h, fill="white", width=4)
space.grid(row = 0, column = 0, rowspan = 200, padx = 10, pady = 10)


# Adding particles with hold and click
space.bind("<B1-Motion>", Particle.add_particle)
space.bind("<Button-1>", Particle.add_particle)


# Settings Title, placement and font
settings_title = ttk.Label(root, text="Experimental Settings")
settings_title.grid(row = 45, column=2, columnspan=40, padx=20)
settings_title.configure(font=("Consolas", 18, "bold"))


# Gravity Slider
# Gravity Slider creation and placement
g_slider = ttk.Scale(root, from_ = 0, to = 30, orient = "horizontal")
g_slider.set(15)
g_slider.grid(row = 75, column = 3, columnspan = 18)

# Gravity Slider Label creation, placement and font
g_label = ttk.Label(root, text="Gravity")
g_label.grid(row = 75, column = 2, padx = 10)
g_label.configure(font=("Consolas", 10, "bold"))

# Gravity Number Labels (low)
g_low = ttk.Label(root, text="1")
g_low.grid(row = 76, column = 3)
g_low.configure(font=("Arial", 9))

# Gravity Number Labels (high)
g_high = ttk.Label(root, text="100")
g_high.grid(row = 76, column = 18)
g_high.configure(font=("Arial", 9))


# Particle Frequency Slider
# Particle Frequency Slider creation and placement
freq_slider = ttk.Scale(root, from_ = 0, to = 20, orient = "horizontal")
freq_slider.set(10)
freq_slider.grid(row = 100, column = 3, padx = 5, columnspan = 18)

# Particle Frequency Label
freq_label = ttk.Label(root, text="Particle Frequency")
freq_label.grid(row = 100, column = 2, padx = 10)
freq_label.configure(font=("Consolas", 10, "bold"))

# Frequency Number Labels (low)
freq_low = ttk.Label(root, text="1")
freq_low.grid(row = 101, column = 3)
freq_low.configure(font=("Arial", 9))

# Frequency Number Labels (high)
freq_high = ttk.Label(root, text="10")
freq_high.grid(row = 101, column = 18)
freq_high.configure(font=("Arial", 9))


# Colour Selection for Particles
options = ["Blue", "Red", "Orange", "Yellow", "Green", "Pink", "Purple", "White"]
# Combobox creation and placement
colour_choose = ttk.Combobox(root, values = options)
colour_choose.current(0)
colour_choose.grid(row = 125, column = 3, padx = 2, columnspan = 23)
# Colour Combobox Label
colour_label = ttk.Label(root, text="Particle Colour")
colour_label.grid(row = 125, column = 2, padx = 2)
colour_label.configure(font=("Consolas", 10, "bold"))


# Reset Button
reset = Button(root, text = "Reset", command = Particle.reset)
reset.grid(row = 150, column = 3)


# Run
root.mainloop()
