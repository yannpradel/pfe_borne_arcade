# Install Ursina engine via pip
# Run the following command in your terminal:
# pip install ursina

from ursina import *
from tkinter import Tk, Label
import threading

# Define the main game class
class EndlessRunnerGame(Entity):
    def __init__(self):
        super().__init__()
        window.title = 'Endless Runner Game with Ursina'
        window.fullscreen = False
        window.size = (1024, 768)
        camera.position = (0, 0, -20)
        camera.rotation = (0, 0, 0)

        self.rectangle_speed = 0.1
        self.height = 0.5
        self.depth = 1.5
        self.left_rectangle_x = -3.0
        self.right_rectangle_x = 3.0
        self.left_start_delay = 3.0
        self.right_start_delay = 2.0
        self.elapsed_time = 0
        self.min_distance_between_rectangles = 2.0
        self.min_distance_from_center_rectangle = 2.0
        self.y = -3.5
        self.reset_distance = 20.0  # Initial reset distance

        self.center_rectangle = Entity(model='cube', color=color.green, position=(0, self.y, 0), scale=(1, self.height, self.depth))
        self.left_rectangle = Entity(model='cube', color=color.green, position=(self.left_rectangle_x, self.y, -5), scale=(1, self.height, self.depth))
        self.right_rectangle = Entity(model='cube', color=color.green, position=(self.right_rectangle_x, self.y, -5), scale=(1, self.height, self.depth))

        self.left_wall = Entity(model='cube', color=color.red, position=(-3.5, 0, -15), scale=(0.5, 10, 100))
        self.right_wall = Entity(model='cube', color=color.red, position=(3.5, 0, -15), scale=(0.5, 10, 100))

        self.speed_text = Text(text=f"Speed: {self.rectangle_speed:.2f}", position=(-0.7, 0.45), scale=2)
        self.height_text = Text(text=f"Height: {self.height:.2f}", position=(-0.7, 0.35), scale=2)
        self.depth_text = Text(text=f"Depth: {self.depth:.2f}", position=(-0.7, 0.25), scale=2)
        self.reset_distance_text = Text(text=f"Reset Distance: {self.reset_distance:.2f}", position=(-0.7, 0.15), scale=2)

        threading.Thread(target=self.display_command_window, daemon=True).start()

    def update(self):
        dt = time.dt
        self.elapsed_time += dt

        if held_keys['up arrow']:
            self.rectangle_speed += 0.01
        if held_keys['down arrow']:
            self.rectangle_speed = max(0.01, self.rectangle_speed - 0.01)
        if held_keys['w']:
            self.height += 0.1
        if held_keys['s']:
            self.height = max(0.1, self.height - 0.1)
        if held_keys['a']:
            self.depth += 0.1
        if held_keys['d']:
            self.depth = max(0.1, self.depth - 0.1)
        if held_keys['k']:
            self.y += 0.1
        if held_keys['i']:
            self.y -= 0.1
        if held_keys['r']:
            self.reset_distance += 1.0
        if held_keys['f']:
            self.reset_distance = max(10.0, self.reset_distance - 1.0)

        if held_keys['j']:
            new_left_x = max(-3.5, self.left_rectangle_x - 0.1)
            if new_left_x < self.right_rectangle_x - self.min_distance_between_rectangles and new_left_x < 0 - self.min_distance_from_center_rectangle:
                self.left_rectangle_x = new_left_x
        if held_keys['l']:
            new_left_x = min(3.5, self.left_rectangle_x + 0.1)
            if new_left_x < self.right_rectangle_x - self.min_distance_between_rectangles and new_left_x < 0 - self.min_distance_from_center_rectangle:
                self.left_rectangle_x = new_left_x
        if held_keys['n']:
            new_right_x = max(-3.5, self.right_rectangle_x - 0.1)
            if new_right_x > self.left_rectangle_x + self.min_distance_between_rectangles and new_right_x > 0 + self.min_distance_from_center_rectangle:
                self.right_rectangle_x = new_right_x
        if held_keys['m']:
            new_right_x = min(3.5, self.right_rectangle_x + 0.1)
            if new_right_x > self.left_rectangle_x + self.min_distance_between_rectangles and new_right_x > 0 + self.min_distance_from_center_rectangle:
                self.right_rectangle_x = new_right_x

        # Update positions
        self.center_rectangle.z -= self.rectangle_speed
        if self.elapsed_time >= self.left_start_delay:
            self.left_rectangle.z -= self.rectangle_speed
        if self.elapsed_time >= self.right_start_delay:
            self.right_rectangle.z -= self.rectangle_speed

        # Reset rectangles
        if self.center_rectangle.z < -self.reset_distance:
            self.center_rectangle.z = 0.0
        if self.left_rectangle.z < -self.reset_distance:
            self.left_rectangle.z = -5.0
        if self.right_rectangle.z < -self.reset_distance:
            self.right_rectangle.z = -5.0

        # Update text
        self.speed_text.text = f"Speed: {self.rectangle_speed:.2f}"
        self.height_text.text = f"Height: {self.height:.2f}"
        self.depth_text.text = f"Depth: {self.depth:.2f}"
        self.reset_distance_text.text = f"Reset Distance: {self.reset_distance:.2f}"

        # Apply transformations
        self.center_rectangle.y = self.y
        self.left_rectangle.y = self.y
        self.right_rectangle.y = self.y
        self.center_rectangle.scale_y = self.height
        self.center_rectangle.scale_z = self.depth
        self.left_rectangle.scale_y = self.height
        self.left_rectangle.scale_z = self.depth
        self.right_rectangle.scale_y = self.height
        self.right_rectangle.scale_z = self.depth
        self.left_rectangle.x = self.left_rectangle_x
        self.right_rectangle.x = self.right_rectangle_x

    def display_command_window(self):
        command_window = Tk()
        command_window.title("Command Information")

        commands = [
            "Controls:",
            "UP    - Increase Speed",
            "DOWN  - Decrease Speed",
            "W     - Increase Height",
            "S     - Decrease Height",
            "A     - Increase Depth",
            "D     - Decrease Depth",
            "J     - Move Left Rectangle Left",
            "L     - Move Left Rectangle Right",
            "N     - Move Right Rectangle Left",
            "M     - Move Right Rectangle Right",
            "K     - Increase View Height (Y)",
            "I     - Decrease View Height (Y)",
            "R     - Increase Reset Distance",
            "F     - Decrease Reset Distance",
            "ESC   - Quit"
        ]

        for command in commands:
            label = Label(command_window, text=command, font=("Arial", 14))
            label.pack()

        command_window.geometry("400x400")
        command_window.mainloop()


if __name__ == '__main__':
    app = Ursina()
    game = EndlessRunnerGame()
    app.run()
