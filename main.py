from tkinter import messagebox
import tkinter as tk
import turtle
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of each snake segment
SEGMENT_WIDTH = 15
SEGMENT_HEIGHT = 15
WIDTH = 500
HEIGHT = 500
SQUARE_SIZE = 24

# Set the margin between each segment
SEGMENT_MARGIN = 3

# Set the size of the game screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg="#111111")
        self.canvas.pack()
        self.food_turtle = turtle.RawTurtle(self.canvas)
        self.food_turtle.hideturtle()
        self.food_turtle.shape('square')
        self.food_turtle.color('red')
        self.food_turtle.penup()
        self.master.bind("<Key>", self.on_key_press)
        self.reset()

    def reset(self):
        self.direction = "Right"
        self.snake_coords = [(SQUARE_SIZE, SQUARE_SIZE), (2 * SQUARE_SIZE, SQUARE_SIZE)]
        self.score = 0
        self.place_food()
        self.update_ui()

    def on_key_press(self, event):
        new_direction = event.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
        if (new_direction in all_directions and
                {new_direction, self.direction} not in opposites):
            self.direction = new_direction

    def place_food(self):
        x = random.randint(0, (WIDTH - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE
        y = random.randint(0, (HEIGHT - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE
        self.food_turtle.goto(x, y)

    def draw_snake(self):
        self.canvas.delete("snake")
        for coord in self.snake_coords:
            x, y = coord
            self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE,
                                          fill="#ffffff", tags="snake")

    def update_ui(self):
        self.draw_snake()
        self.master.after(100, self.update)

    def move_snake(self):
        head_x, head_y = self.snake_coords[-1]
        if self.direction == "Up":
            new_head_coords = (head_x, head_y - SQUARE_SIZE)
        elif self.direction == "Down":
            new_head_coords = (head_x, head_y + SQUARE_SIZE)
        elif self.direction == "Left":
            new_head_coords = (head_x - SQUARE_SIZE, head_y)
        elif self.direction == "Right":
            new_head_coords = (head_x + SQUARE_SIZE, head_y)
        self.snake_coords.append(new_head_coords)
        if self.food_turtle.distance(*self.snake_coords[-1]) < SQUARE_SIZE:
            self.score += 10
            self.place_food()
        else:
            self.snake_coords.pop(0)


    def check_collisions(self):
        head_x, head_y = self.snake_coords[-1]
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        for coord in self.snake_coords[:-1]:
            if coord == (head_x, head_y):
                return True
        return False

    def update(self):
        self.move_snake()
        if self.check_collisions():
            messagebox.showinfo("Game Over", f"Your score is {self.score}")
            self.reset()
        else:
            self.update_ui()
            self.master.after(400, self.update)

    def start(self):
        self.food_image = tk.PhotoImage(file="food.png")
        self.update()
        self.master.mainloop()






root = tk.Tk()
root.title("Snake Game")


snake = SnakeGame(root)



# Run the event loop
root.mainloop()