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

        # Sliders for controlling parameters
        self.left_rectangle_x = -3.30
        self.left_rectangle_x_slider = Slider(min=-5.0, max=5.0, default=self.left_rectangle_x, position=(-0.7, -0.15 * 0.7), text='Left Rectangle X', scale=0.7, dynamic=True)
        self.right_rectangle_x = 3.30
        self.right_rectangle_x_slider = Slider(min=-5.0, max=5.0, default=self.right_rectangle_x, position=(-0.7, -0.25 * 0.7), text='Right Rectangle X', scale=0.7, dynamic=True)
        self.y = -5.0
        self.y_position_slider = Slider(min=-5.0, max=5.0, default=self.y, position=(-0.7, -0.35 * 0.7), text='Y Position', scale=0.7, dynamic=True)
        self.rectangle_speed = 0.1
        self.speed_slider = Slider(min=0.01, max=1.0, default=self.rectangle_speed, position=(-0.7, 0.35 * 0.7), text='Speed', scale=0.7, dynamic=True)
        self.height = 0.5
        self.height_slider = Slider(min=0.1, max=10.0, default=self.height, position=(-0.7, 0.25 * 0.7), text='Height', scale=0.7, dynamic=True)
        self.depth = 8.0
        self.depth_slider = Slider(min=0.1, max=10.0, default=self.depth, position=(-0.7, 0.15 * 0.7), text='Depth', scale=0.7, dynamic=True)
        self.width = 2.5
        self.width_slider = Slider(min=0.1, max=10.0, default=self.width, position=(-0.7, 0.05 * 0.7), text='Width', scale=0.7, dynamic=True)
        self.reset_distance = 20.0
        self.reset_distance_slider = Slider(min=10.0, max=50.0, default=self.reset_distance, position=(-0.7, -0.05 * 0.7), text='Reset Distance', scale=0.7, dynamic=True)
        self.spawn_distance = 40.0
        self.spawn_distance_slider = Slider(min=20.0, max=60.0, default=self.spawn_distance, position=(-0.7, 0.45 * 0.7), text='Spawn Distance', scale=0.7, dynamic=True)
        self.left_wall_position_slider = Slider(min=-5.0, max=5.0, default=-5.0, position=(-0.7, -0.45 * 0.7), text='Left Wall Position', scale=0.7, dynamic=True)
        self.right_wall_position_slider = Slider(min=-5.0, max=5.0, default=5, position=(-0.7, -0.55 * 0.7), text='Right Wall Position', scale=0.7, dynamic=True)
        window.title = 'Endless Runner Game with Ursina'
        window.fullscreen = False
        window.size = (1280, 720)
        camera.position = (0, 0, -20)
        camera.rotation = (0, 0, 0)

        self.rectangle_speed = 0.1
        self.height = 0.5
        self.depth = 1.5
        self.width = 1.0
        self.left_rectangle_x = -3.3
        self.right_rectangle_x = 3.3
        self.left_start_delay = 3.0
        self.right_start_delay = 2.0
        self.elapsed_time = 0
        self.min_distance_between_rectangles = 2.0
        self.min_distance_from_center_rectangle = 2.0
        self.y = 5.0
        self.reset_distance = 20.0  # Initial reset distance
        self.spawn_distance = 40.0  # Initial spawn distance

        self.center_rectangle = Entity(model='cube', texture='brick', color=color.green, position=(0, self.y, self.spawn_distance), scale=(self.width, self.height, self.depth))
        self.left_rectangle = Entity(model='cube', texture='brick', color=color.azure, position=(self.left_rectangle_x, self.y, self.spawn_distance - 5), scale=(self.width, self.height, self.depth))
        self.right_rectangle = Entity(model='cube', texture='brick', color=color.orange, position=(self.right_rectangle_x, self.y, self.spawn_distance - 5), scale=(self.width, self.height, self.depth))

        self.left_wall = Entity(model='cube', texture='white_cube', color=color.red, position=(-5.0, 0, -15), scale=(0.5, 10, 100))
        self.right_wall = Entity(model='cube', texture='white_cube', color=color.red, position=(5.0, 0, -15), scale=(0.5, 10, 100))

        # Removed command window in favor of sliders

    def update(self):
        # Update parameters from sliders
        self.left_rectangle_x = self.left_rectangle_x_slider.value
        self.right_rectangle_x = self.right_rectangle_x_slider.value
        self.y = self.y_position_slider.value
        self.rectangle_speed = self.speed_slider.value
        self.height = self.height_slider.value
        self.depth = self.depth_slider.value
        self.reset_distance = self.reset_distance_slider.value
        self.spawn_distance = self.spawn_distance_slider.value
        self.left_wall.x = self.left_wall_position_slider.value
        self.right_wall.x = self.right_wall_position_slider.value
        dt = time.dt
        self.elapsed_time += dt

        # Update positions
        self.center_rectangle.z -= self.rectangle_speed
        if self.elapsed_time >= self.left_start_delay:
            self.left_rectangle.z -= self.rectangle_speed
        if self.elapsed_time >= self.right_start_delay:
            self.right_rectangle.z -= self.rectangle_speed

        # Reset rectangles
        if self.center_rectangle.z < -self.reset_distance:
            self.center_rectangle.z = self.spawn_distance
        if self.left_rectangle.z < -self.reset_distance:
            self.left_rectangle.z = self.spawn_distance - 5
        if self.right_rectangle.z < -self.reset_distance:
            self.right_rectangle.z = self.spawn_distance - 5

        # Apply transformations
        self.center_rectangle.y = self.y
        self.left_rectangle.y = self.y
        self.right_rectangle.y = self.y
        self.width = self.width_slider.value
        self.center_rectangle.scale_x = self.width
        self.center_rectangle.scale_y = self.height
        self.center_rectangle.scale_z = self.depth
        self.left_rectangle.scale_x = self.width
        self.left_rectangle.scale_y = self.height
        self.left_rectangle.scale_z = self.depth
        self.right_rectangle.scale_x = self.width
        self.right_rectangle.scale_y = self.height
        self.right_rectangle.scale_z = self.depth
        self.left_rectangle.x = self.left_rectangle_x
        self.right_rectangle.x = self.right_rectangle_x

if __name__ == '__main__':
    app = Ursina()
    game = EndlessRunnerGame()
    app.run()
