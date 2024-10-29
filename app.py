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
        self.platforms = []  # Store all platforms
        self.phase_executed = False  # Track if platforms for the phase have been sent

    def initialize_sliders(self):
        # Initialize UI sliders for controlling game parameters
        self.spawn_distance_slider = Slider(min=20.0, max=60.0, default=50.0, position=(-0.7, 0.45 * 0.7), text='Spawn Distance', scale=0.7, dynamic=True)
        self.speed_slider = Slider(min=0.01, max=1.0, default=0.15, position=(-0.7, 0.35 * 0.7), text='Speed', scale=0.7, dynamic=True)
        self.height_slider = Slider(min=0.1, max=10.0, default=0.5, position=(-0.7, 0.25 * 0.7), text='Height', scale=0.7, dynamic=True)
        self.depth_slider = Slider(min=0.1, max=10.0, default=8.0, position=(-0.7, 0.15 * 0.7), text='Depth', scale=0.7, dynamic=True)
        self.width_slider = Slider(min=0.1, max=10.0, default=2.5, position=(-0.7, 0.05 * 0.7), text='Width', scale=0.7, dynamic=True)
        self.reset_distance_slider = Slider(min=10.0, max=50.0, default=10.0, position=(-0.7, -0.05 * 0.7), text='Reset Distance', scale=0.7, dynamic=True)
        self.y_position_slider = Slider(min=-5.0, max=5.0, default=-5.0, position=(-0.7, -0.35 * 0.7), text='Y Position', scale=0.7, dynamic=True)
        self.left_wall_position_slider = Slider(min=-10.0, max=10.0, default=-5.0, position=(-0.7, -0.45 * 0.7), text='Left Wall Position', scale=0.7, dynamic=True)
        self.right_wall_position_slider = Slider(min=-10.0, max=10.0, default=5.0, position=(-0.7, -0.55 * 0.7), text='Right Wall Position', scale=0.7, dynamic=True)

    def initialize_game_entities(self):
        # Initialize game entities like walls and player
        self.left_wall = Entity(model='cube', texture='white_cube', color=color.red, position=(-5.0, 0, -15), scale=(0.5, 10, 100))
        self.right_wall = Entity(model='cube', texture='white_cube', color=color.red, position=(5.0, 0, -15), scale=(0.5, 10, 100))
        self.player = Entity(model='cube', texture='whatsapp', color=color.yellow, position=(0, self.y_position_slider.value + 1.25, 40.0), scale=(0.5, 0.5, 0.5))
        self.player.jumping = False
        self.player.velocity_y = 0  # Vertical velocity for player

    def setup_camera(self):
        # Configure the camera settings
        window.title = 'Endless Runner Game with Ursina'
        window.fullscreen = False
        window.size = (1280, 720)
        camera.position = (0, 0, -20)
        camera.rotation = (0, 0, 0)

    def create_platform(self, position, scale, color=color.white):
        # Ensure platforms do not exceed wall boundaries
        left_limit = self.left_wall.x + self.left_wall.scale_x / 2
        right_limit = self.right_wall.x - self.right_wall.scale_x / 2
        print(f'Left wall x: {self.left_wall.x}, Right wall x: {self.right_wall.x}, Platform position: {position}')

        # Adjust position to prevent exceeding boundaries
        if position[0] - scale[0] / 2 < left_limit:
            position = (left_limit + scale[0] / 2, position[1], position[2])
        if position[0] + scale[0] / 2 > right_limit:
            position = (right_limit - scale[0] / 2, position[1], position[2])
        print(f'Adjusted Platform position: {position}')
        
        # Create a platform entity
        platform = Entity(model='cube', texture='brick', color=color, position=position, scale=scale)
        self.platforms.append(platform)

    def update(self):
        self.phase_text.text = f'Phase: {self.current_phase}'
        self.update_parameters_from_sliders()
        self.handle_player_movement()
        self.apply_gravity()
        self.update_phase_logic()
        self.update_platform_positions()

    def update_parameters_from_sliders(self):
        # Update game parameters based on slider values
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
            on_platform = None
            for platform in self.platforms:
                if (platform.z - platform.scale_z / 2 <= self.player.z <= platform.z + platform.scale_z / 2 and
                        platform.x - platform.scale_x / 2 <= self.player.x <= platform.x + platform.scale_x / 2):
                    on_platform = platform
                    break
            if on_platform:
                self.player.y = on_platform.y + on_platform.scale_y / 2 + 0.25
                self.player.velocity_y = 0
            else:
                self.player.velocity_y += self.gravity * dt
                self.player.y += self.player.velocity_y * dt
        else:
            self.player.velocity_y += self.gravity * dt
            self.player.y += self.player.velocity_y * dt
            if self.player.y <= self.y + self.height / 2 + 0.25 and self.player.velocity_y < 0:
                self.player.jumping = False
                self.player.y = self.y + self.height / 2 + 0.25
                self.player.velocity_y = 0

    def update_phase_logic(self):
        # Handle phase transitions
        current_time = time.time()
        if self.current_phase == 'single_platform' and not self.phase_executed:
            # Create a very long and wide platform for initial movement
            self.create_platform(position=(0, self.y, self.spawn_distance), scale=(20, 2, 50), color=color.green)
            self.player.y = self.y + 1.25  # Position player on top of the platform
            self.phase_executed = True
        elif self.current_phase == 'multiple_platforms' and not self.phase_executed:
            # Clear existing platforms
            for platform in self.platforms:
                destroy(platform)
            self.platforms.clear()
            # Create three small platforms: left, middle, right
            self.create_platform(position=(-3.3, self.y, self.spawn_distance), scale=(1, self.height, self.depth), color=color.azure)
            self.create_platform(position=(0, self.y, self.spawn_distance), scale=(1, self.height, self.depth), color=color.yellow)
            self.create_platform(position=(3.3, self.y, self.spawn_distance), scale=(1, self.height, self.depth), color=color.orange)
            self.phase_executed = True

        # Update to next phase if platforms are no longer in view
        if self.current_phase == 'single_platform':
            for platform in self.platforms:
                if platform.z < -30:  # Assuming -30 is out of view
                    self.current_phase = 'multiple_platforms'
                    self.phase_start_time = current_time
                    self.phase_executed = False
                    break

    def update_platform_positions(self):
        # Update the positions of platforms based on the game phase
        dt = time.dt * 20  # Increase the speed of platform movement
        for platform in self.platforms:
            platform.z -= self.rectangle_speed * dt

if __name__ == '__main__':
    app = Ursina()
    game = EndlessRunnerGame()
    app.run()
