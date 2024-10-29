# Install Ursina engine via pip
# Run the following command in your terminal:
# pip install ursina

from ursina import *
import time

class EndlessRunnerGame(Entity):
    def __init__(self):
        super().__init__()
        self.initialize_sliders()
        self.initialize_game_entities()
        self.setup_camera()
        
        self.current_phase = 'single_platform'
        self.phase_text = Text(text=f'Phase: {self.current_phase}', position=(0.7, 0.45), origin=(0, 0), scale=1.5, color=color.white)
        self.phase_start_time = time.time()
        self.elapsed_time = 0
        self.player_speed = 5.0
        self.gravity = -9.8  # Gravity acceleration

    def initialize_sliders(self):
        # Initialize UI sliders for controlling game parameters
        self.left_rectangle_x_slider = Slider(min=-5.0, max=5.0, default=-3.30, position=(-0.7, -0.15 * 0.7), text='Left Rectangle X', scale=0.7, dynamic=True)
        self.right_rectangle_x_slider = Slider(min=-5.0, max=5.0, default=3.30, position=(-0.7, -0.25 * 0.7), text='Right Rectangle X', scale=0.7, dynamic=True)
        self.y_position_slider = Slider(min=-5.0, max=5.0, default=-5.0, position=(-0.7, -0.35 * 0.7), text='Y Position', scale=0.7, dynamic=True)
        self.speed_slider = Slider(min=0.01, max=1.0, default=0.15, position=(-0.7, 0.35 * 0.7), text='Speed', scale=0.7, dynamic=True)
        self.height_slider = Slider(min=0.1, max=10.0, default=0.5, position=(-0.7, 0.25 * 0.7), text='Height', scale=0.7, dynamic=True)
        self.depth_slider = Slider(min=0.1, max=10.0, default=8.0, position=(-0.7, 0.15 * 0.7), text='Depth', scale=0.7, dynamic=True)
        self.width_slider = Slider(min=0.1, max=10.0, default=2.5, position=(-0.7, 0.05 * 0.7), text='Width', scale=0.7, dynamic=True)
        self.reset_distance_slider = Slider(min=10.0, max=50.0, default=10.0, position=(-0.7, -0.05 * 0.7), text='Reset Distance', scale=0.7, dynamic=True)
        self.spawn_distance_slider = Slider(min=20.0, max=60.0, default=50.0, position=(-0.7, 0.45 * 0.7), text='Spawn Distance', scale=0.7, dynamic=True)
        self.left_wall_position_slider = Slider(min=-5.0, max=5.0, default=-5.0, position=(-0.7, -0.45 * 0.7), text='Left Wall Position', scale=0.7, dynamic=True)
        self.right_wall_position_slider = Slider(min=-5.0, max=5.0, default=5.0, position=(-0.7, -0.55 * 0.7), text='Right Wall Position', scale=0.7, dynamic=True)

    def initialize_game_entities(self):
        # Initialize game entities like walls, rectangles, and player
        self.center_rectangle = Entity(model='cube', texture='brick', color=color.green, position=(0, -5.0, 50.0), scale=(2.5, 0.5, 8.0))
        self.left_rectangle = Entity(model='cube', texture='brick', color=color.azure, position=(-3.30, -5.0, 45.0), scale=(2.5, 0.5, 8.0))
        self.right_rectangle = Entity(model='cube', texture='brick', color=color.orange, position=(3.30, -5.0, 45.0), scale=(2.5, 0.5, 8.0))
        self.left_wall = Entity(model='cube', texture='white_cube', color=color.red, position=(-5.0, 0, -15), scale=(0.5, 10, 100))
        self.right_wall = Entity(model='cube', texture='white_cube', color=color.red, position=(5.0, 0, -15), scale=(0.5, 10, 100))
        self.player = Entity(model='cube', texture='whatsapp', color=color.yellow, position=(0, -4.75, 40.0), scale=(0.5, 0.5, 0.5))
        self.player.jumping = False
        self.player.velocity_y = 0  # Vertical velocity for player

    def setup_camera(self):
        # Configure the camera settings
        window.title = 'Endless Runner Game with Ursina'
        window.fullscreen = False
        window.size = (1280, 720)
        camera.position = (0, 0, -20)
        camera.rotation = (0, 0, 0)

    def update(self):
        self.phase_text.text = f'Phase: {self.current_phase}'
        self.update_parameters_from_sliders()
        self.handle_player_movement()
        self.apply_gravity()
        self.update_phase_logic()
        self.update_rectangle_positions()
        self.update_game_entities()

    def update_parameters_from_sliders(self):
        # Update game parameters based on slider values
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

    def handle_player_movement(self):
        dt = time.dt
        if held_keys['left arrow']:
            self.player.x -= self.player_speed * dt
            self.player.rotation_y = 90
        if held_keys['right arrow']:
            self.player.x += self.player_speed * dt
            self.player.rotation_y = -90
        if held_keys['up arrow']:
            self.player.z += self.player_speed * 1.5 * dt
            self.player.rotation_y = 0
        if held_keys['down arrow']:
            self.player.z -= self.player_speed * 1.5 * dt
            self.player.rotation_y = 180
        if held_keys['space'] and not self.player.jumping:
            self.player.jumping = True
            self.player.velocity_y = 5  # Initial jump velocity

    def apply_gravity(self):
        # Apply gravity to the player
        dt = time.dt
        if not self.player.jumping:
            on_platform = (
                (self.center_rectangle.z - self.depth / 2 <= self.player.z <= self.center_rectangle.z + self.depth / 2 and
                 self.center_rectangle.x - self.width / 2 <= self.player.x <= self.center_rectangle.x + self.width / 2) or
                (self.left_rectangle.z - self.depth / 2 <= self.player.z <= self.left_rectangle.z + self.depth / 2 and
                 self.left_rectangle.x - self.width / 2 <= self.player.x <= self.left_rectangle.x + self.width / 2) or
                (self.right_rectangle.z - self.depth / 2 <= self.player.z <= self.right_rectangle.z + self.depth / 2 and
                 self.right_rectangle.x - self.width / 2 <= self.player.x <= self.right_rectangle.x + self.width / 2)
            )
            if on_platform:
                self.player.y = self.y + self.height / 2 + 0.25
                self.player.velocity_y = 0
            else:
                self.player.velocity_y += self.gravity * dt
                self.player.y += self.player.velocity_y * dt
        else:
            self.player.velocity_y += self.gravity * dt
            self.player.y += self.player.velocity_y * dt
            if self.player.y <= self.y + self.height / 2 + 0.25:
                self.player.jumping = False
                self.player.y = self.y + self.height / 2 + 0.25
                self.player.velocity_y = 0

    def update_phase_logic(self):
        # Handle phase transitions
        current_time = time.time()
        if self.current_phase == 'single_platform' and current_time - self.phase_start_time > 5:
            self.current_phase = 'multiple_platforms'
            self.phase_start_time = current_time

    def update_rectangle_positions(self):
        # Update the positions of rectangles based on the game phase
        dt = time.dt
        self.elapsed_time += dt
        if self.current_phase == 'single_platform':
            self.center_rectangle.z -= self.rectangle_speed * 0.2
            self.left_rectangle.z -= self.rectangle_speed * 0.2
            self.right_rectangle.z -= self.rectangle_speed * 0.2
        elif self.current_phase == 'multiple_platforms':
            self.center_rectangle.z -= self.rectangle_speed
            if self.elapsed_time >= 3.0:
                self.left_rectangle.z -= self.rectangle_speed
            if self.elapsed_time >= 2.0:
                self.right_rectangle.z -= self.rectangle_speed
            self.reset_rectangles()

    def reset_rectangles(self):
        # Reset rectangles if they go beyond the reset distance
        if self.center_rectangle.z < -self.reset_distance:
            self.center_rectangle.z = self.spawn_distance
        if self.left_rectangle.z < -self.reset_distance:
            self.left_rectangle.z = self.spawn_distance - 5
        if self.right_rectangle.z < -self.reset_distance:
            self.right_rectangle.z = self.spawn_distance - 5

    def update_game_entities(self):
        # Update game entities' positions and scales based on slider values
        self.center_rectangle.position = (0, self.y, self.center_rectangle.z)
        self.left_rectangle.position = (self.left_rectangle_x, self.y, self.left_rectangle.z)
        self.right_rectangle.position = (self.right_rectangle_x, self.y, self.right_rectangle.z)
        for rectangle in [self.center_rectangle, self.left_rectangle, self.right_rectangle]:
            rectangle.scale = (self.width, self.height, self.depth)

if __name__ == '__main__':
    app = Ursina()
    game = EndlessRunnerGame()
    app.run()
