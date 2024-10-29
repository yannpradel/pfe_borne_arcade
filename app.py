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
        self.rectangle_speed = 0.15
        self.speed_slider = Slider(min=0.01, max=1.0, default=self.rectangle_speed, position=(-0.7, 0.35 * 0.7), text='Speed', scale=0.7, dynamic=True)
        self.height = 0.5
        self.height_slider = Slider(min=0.1, max=10.0, default=self.height, position=(-0.7, 0.25 * 0.7), text='Height', scale=0.7, dynamic=True)
        self.depth = 8.0
        self.depth_slider = Slider(min=0.1, max=10.0, default=self.depth, position=(-0.7, 0.15 * 0.7), text='Depth', scale=0.7, dynamic=True)
        self.width = 2.5
        self.width_slider = Slider(min=0.1, max=10.0, default=self.width, position=(-0.7, 0.05 * 0.7), text='Width', scale=0.7, dynamic=True)
        self.reset_distance = 10.0
        self.reset_distance_slider = Slider(min=10.0, max=50.0, default=self.reset_distance, position=(-0.7, -0.05 * 0.7), text='Reset Distance', scale=0.7, dynamic=True)
        self.spawn_distance = 50.0
        self.spawn_distance_slider = Slider(min=20.0, max=60.0, default=self.spawn_distance, position=(-0.7, 0.45 * 0.7), text='Spawn Distance', scale=0.7, dynamic=True)
        self.left_wall_position_slider = Slider(min=-5.0, max=5.0, default=-5.0, position=(-0.7, -0.45 * 0.7), text='Left Wall Position', scale=0.7, dynamic=True)
        self.right_wall_position_slider = Slider(min=-5.0, max=5.0, default=5, position=(-0.7, -0.55 * 0.7), text='Right Wall Position', scale=0.7, dynamic=True)
        window.title = 'Endless Runner Game with Ursina'
        window.fullscreen = False
        window.size = (1280, 720)
        camera.position = (0, 0, -20)
        camera.rotation = (0, 0, 0)

        self.rectangle_speed = 0.15
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
        self.phase_start_time = time.time()
        self.current_phase = 'single_platform'

        self.center_rectangle = Entity(model='cube', texture='brick', color=color.green, position=(0, self.y, self.spawn_distance), scale=(self.width, self.height, self.depth))
        self.left_rectangle = Entity(model='cube', texture='brick', color=color.azure, position=(self.left_rectangle_x, self.y, self.spawn_distance - 5), scale=(self.width, self.height, self.depth))
        self.right_rectangle = Entity(model='cube', texture='brick', color=color.orange, position=(self.right_rectangle_x, self.y, self.spawn_distance - 5), scale=(self.width, self.height, self.depth))

        self.left_wall = Entity(model='cube', texture='white_cube', color=color.red, position=(-5.0, 0, -15), scale=(0.5, 10, 100))
        self.right_wall = Entity(model='cube', texture='white_cube', color=color.red, position=(5.0, 0, -15), scale=(0.5, 10, 100))

        self.player = Entity(model='cube', texture='whatsapp', color=color.yellow, position=(0, self.y + self.height / 2 + 0.25, self.spawn_distance - 10), scale=(0.5, 0.5, 0.5))
        self.player.jumping = False
        self.player_speed = 5.0

        # Removed command window in favor of sliders

    def update(self):
        def end_jump():
            self.player.jumping = False
            self.player.y = self.y + self.height / 2 + 0.25
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
        self.width = self.width_slider.value
        dt = time.dt
        self.elapsed_time += dt

        # Phase transition logic
        current_time = time.time()
        if self.current_phase == 'single_platform' and current_time - self.phase_start_time > 5:
            self.current_phase = 'multiple_platforms'
            self.phase_start_time = current_time

        # Player movement
        if held_keys['left arrow']:
            self.player.x -= self.player_speed * dt
            self.player.rotation_y = 90
            self.player.look_at(self.player.position + Vec3(-1, 0, 0))
        if held_keys['right arrow']:
            self.player.x += self.player_speed * dt
            self.player.rotation_y = -90
            self.player.look_at(self.player.position + Vec3(1, 0, 0))
        if held_keys['space']:
            if not self.player.jumping:
                self.player.jumping = True
                self.player.animate_y(self.player.y + 3, duration=0.3, curve=curve.out_expo)
                invoke(self.player.animate_y, self.player.y, duration=0.3, delay=0.3, curve=curve.in_expo)
                invoke(end_jump, delay=0.6)
        if held_keys['down arrow']:
            self.player.z -= self.player_speed * 1.5 * dt
            self.player.rotation_y = 180
            self.player.look_at(self.player.position + Vec3(0, 0, -1))

        if held_keys['left arrow']:
            self.player.x -= self.player_speed * dt
        if held_keys['right arrow']:
            self.player.x += self.player_speed * dt
        if held_keys['up arrow']:
            self.player.z += self.player_speed * 1.5 * dt
        if held_keys['down arrow']:
            self.player.z -= self.player_speed * 1.5 * dt

        if self.current_phase == 'single_platform':
            if held_keys['left arrow']:
                self.player.x -= self.player_speed * dt
            if held_keys['right arrow']:
                self.player.x += self.player_speed * dt

        # Ensure player stays above the platform
        if not self.player.jumping:
            self.player.y = self.y + self.height / 2 + 0.25

        # Update positions based on phase
        if self.current_phase == 'single_platform':
            self.center_rectangle.z -= self.rectangle_speed * 0.5
            self.left_rectangle.z -= self.rectangle_speed * 0.5
            self.right_rectangle.z -= self.rectangle_speed * 0.5

        if self.current_phase == 'multiple_platforms':
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
