# Install Ursina engine via pip
# Run the following command in your terminal:
# pip install ursina

from ursina import *
import time

class EndlessRunnerGame(Entity):
    def __init__(self):
        super().__init__()
        self.player_speed = 5.0
        self.platform_speed = 0.15
        self.gravity = -9.8
        self.platforms = []
        self.initialize_game()
        self.setup_camera()

    def initialize_game(self):
        # Create player
        self.player = Entity(model='cube', color=color.yellow, position=(0, 1, -10), scale=(1, 1, 1))
        self.player.velocity_y = 0
        self.player.jumping = False

        # Create initial platform
        self.create_platform(position=(0, 0, 0), scale=(20, 1, 50), color=color.green)

        # Create walls
        self.left_wall = Entity(model='cube', color=color.red, position=(-10, 5, 0), scale=(1, 10, 100))
        self.right_wall = Entity(model='cube', color=color.red, position=(10, 5, 0), scale=(1, 10, 100))

    def setup_camera(self):
        window.title = 'Endless Runner Game'
        window.fullscreen = False
        window.size = (1280, 720)
        camera.position = (0, 10, -30)
        camera.rotation = (30, 0, 0)

    def create_platform(self, position, scale, color=color.white):
        platform = Entity(model='cube', texture='brick', color=color, position=position, scale=scale)
        self.platforms.append(platform)

    def update(self):
        self.handle_player_movement()
        self.apply_gravity()
        self.update_platforms()

    def handle_player_movement(self):
        dt = time.dt
        if held_keys['left arrow']:
            self.player.x -= self.player_speed * dt
        if held_keys['right arrow']:
            self.player.x += self.player_speed * dt
        if held_keys['space'] and not self.player.jumping:
            self.player.jumping = True
            self.player.velocity_y = 5

    def apply_gravity(self):
        dt = time.dt
        self.player.velocity_y += self.gravity * dt
        self.player.y += self.player.velocity_y * dt

        # Check if player is on a platform
        on_platform = False
        for platform in self.platforms:
            if platform.z - platform.scale_z / 2 <= self.player.z <= platform.z + platform.scale_z / 2 and \
                    platform.x - platform.scale_x / 2 <= self.player.x <= platform.x + platform.scale_x / 2 and \
                    self.player.y <= platform.y + platform.scale_y:
                self.player.y = platform.y + platform.scale_y
                self.player.velocity_y = 0
                self.player.jumping = False
                on_platform = True
                break

        if not on_platform and self.player.y <= 0:
            self.player.y = 0
            self.player.velocity_y = 0
            self.player.jumping = False

    def update_platforms(self):
        dt = time.dt
        for platform in self.platforms:
            platform.z += self.platform_speed * dt
            if platform.z > 20:
                destroy(platform)
                self.platforms.remove(platform)
                # Create a new platform
                self.create_platform(position=(0, 0, -50), scale=(20, 1, 50), color=color.green)

        # Move walls
        self.left_wall.z += self.platform_speed * dt
        self.right_wall.z += self.platform_speed * dt
        if self.left_wall.z > 20:
            self.left_wall.z = -50
            self.right_wall.z = -50

if __name__ == '__main__':
    app = Ursina()
    game = EndlessRunnerGame()
    app.run()
