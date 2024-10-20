import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame.freetype
import tkinter as tk
from tkinter import Label

# Initial parameters for the rectangles
y = -3.5  # Position at the bottom of the screen (Y)
rectangle_z = 0.0    # Initial depth position of the center rectangle
rectangle_speed = 0.1  # Initial speed of depth movement  # Initial speed of depth movement
height = 0.5  # Set initial height to be minimal  # Initial height of the rectangles
depth = 1.5  # Set depth to be slightly longer    # Initial depth of the rectangles

# Left and right rectangles positions
left_rectangle_z = -5.0
left_rectangle_x = -3.0
right_rectangle_z = -5.0
right_rectangle_x = 3.0

# Delay for left and right rectangles to start moving
left_start_delay = 3.0  # Seconds
right_start_delay = 2.0  # Seconds

# Boundaries for the left and right movement
left_boundary = -3.5
right_boundary = 3.5

# Walls for the game boundaries
def draw_walls():
    """Draw left and right walls extending along the Z-axis."""
    glBegin(GL_QUADS)

    # Left wall
    glColor3f(0.8, 0.1, 0.1)  # Red color for the wall
    glVertex3f(left_boundary - 0.5, -5.0, 20.0)
    glVertex3f(left_boundary, -5.0, 20.0)
    glVertex3f(left_boundary, 5.0, -50.0)
    glVertex3f(left_boundary - 0.5, 5.0, -50.0)

    # Right wall
    glColor3f(0.8, 0.1, 0.1)  # Red color for the wall
    glVertex3f(right_boundary, -5.0, 20.0)
    glVertex3f(right_boundary + 0.5, -5.0, 20.0)
    glVertex3f(right_boundary + 0.5, 5.0, -50.0)
    glVertex3f(right_boundary, 5.0, -50.0)

    glEnd()

# Minimum distance between the rectangles
min_distance_between_rectangles = 2.0
min_distance_from_center_rectangle = 2.0

# Initialize font for text rendering
pygame.freetype.init()
font = pygame.freetype.SysFont(None, 36)  # Default font, size 36

def draw_rectangle(x, y, z, width=1.0, height=0.5, depth=1.0):
    """Draw a 3D rectangle with specified x, y, z positions, width, height, and depth."""
    glBegin(GL_QUADS)

    # Front face
    glColor3f(0.4, 0.8, 0.4)
    glVertex3f(x - width, y, z + depth)
    glVertex3f(x + width, y, z + depth)
    glVertex3f(x + width, y + height, z + depth)
    glVertex3f(x - width, y + height, z + depth)

    # Back face
    glColor3f(0.4, 0.8, 0.4)
    glVertex3f(x - width, y, z - depth)
    glVertex3f(x - width, y + height, z - depth)
    glVertex3f(x + width, y + height, z - depth)
    glVertex3f(x + width, y, z - depth)

    # Bottom face
    glColor3f(0.4, 0.8, 0.4)
    glVertex3f(x - width, y, z - depth)
    glVertex3f(x + width, y, z - depth)
    glVertex3f(x + width, y, z + depth)
    glVertex3f(x - width, y, z + depth)

    # Top face
    glColor3f(0.4, 0.8, 0.4)
    glVertex3f(x - width, y + height, z + depth)
    glVertex3f(x + width, y + height, z + depth)
    glVertex3f(x + width, y + height, z - depth)
    glVertex3f(x - width, y + height, z - depth)

    # Side faces
    glColor3f(0.5, 0.1, 0.5)
    glVertex3f(x + width, y, z + depth)
    glVertex3f(x + width, y + height, z + depth)
    glVertex3f(x + width, y + height, z - depth)
    glVertex3f(x + width, y, z - depth)

    glVertex3f(x - width, y, z + depth)
    glVertex3f(x - width, y, z - depth)
    glVertex3f(x - width, y + height, z - depth)
    glVertex3f(x - width, y + height, z + depth)

    glEnd()

def render_text(text, x, y, surface, font, color=(255, 255, 255)):
    """Render text in the specified Pygame surface using pygame.freetype."""
    font.render_to(surface, (x, y), text, color)

def display_command_window():
    """Create a second window using Tkinter to display available keyboard commands."""
    command_window = tk.Tk()
    command_window.title("Command Information")
    
    # Command list
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
        "ESC   - Quit"
    ]
    
    # Add commands to the window
    for command in commands:
        label = Label(command_window, text=command, font=("Arial", 14))
        label.pack()

    command_window.geometry("400x400")
    command_window.mainloop()

def main():
    global rectangle_z, left_rectangle_z, right_rectangle_z, rectangle_speed, height, depth
    global left_rectangle_x, right_rectangle_x, y

    pygame.init()

    # OpenGL Window
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('OpenGL Window with Parameters')

    glClearColor(0.2, 0.2, 0.6, 1.0)  # Background color for OpenGL (blueish)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Perspective
    glTranslatef(0.0, 0.0, -5)  # Camera position

    # Launch the Tkinter command window in a separate thread
    import threading
    threading.Thread(target=display_command_window, daemon=True).start()

    clock = pygame.time.Clock()
    elapsed_time = 0.0  # Elapsed time to manage delays

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()

        # Keyboard input to modify parameters
        if keys[K_UP]:
            rectangle_speed += 0.01  # Increase speed
        if keys[K_DOWN]:
            rectangle_speed = max(0.01, rectangle_speed - 0.01)  # Decrease speed, minimum 0.01
        if keys[K_w]:
            height += 0.1  # Increase height
        if keys[K_s]:
            height = max(0.1, height - 0.1)  # Decrease height, minimum 0.1
        if keys[K_a]:
            depth += 0.1  # Increase depth
        if keys[K_d]:
            depth = max(0.1, depth - 0.1)  # Decrease depth, minimum 0.1
        if keys[K_j]:
            new_left_x = max(left_boundary, left_rectangle_x - 0.1)  # Calculate new position for left rectangle
            if new_left_x < right_rectangle_x - min_distance_between_rectangles and new_left_x < 0 - min_distance_from_center_rectangle:
                left_rectangle_x = new_left_x  # Update position if no collision
        if keys[K_l]:
            new_left_x = min(right_boundary, left_rectangle_x + 0.1)  # Calculate new position for left rectangle
            if new_left_x < right_rectangle_x - min_distance_between_rectangles and new_left_x < 0 - min_distance_from_center_rectangle:
                left_rectangle_x = new_left_x  # Update position if no collision
        if keys[K_n]:
            new_right_x = max(left_boundary, right_rectangle_x - 0.1)  # Calculate new position for right rectangle
            if new_right_x > left_rectangle_x + min_distance_between_rectangles and new_right_x > 0 + min_distance_from_center_rectangle:
                right_rectangle_x = new_right_x  # Update position if no collision
        if keys[K_m]:
            new_right_x = min(right_boundary, right_rectangle_x + 0.1)  # Calculate new position for right rectangle
            if new_right_x > left_rectangle_x + min_distance_between_rectangles and new_right_x > 0 + min_distance_from_center_rectangle:
                right_rectangle_x = new_right_x  # Update position if no collision
        if keys[K_k]:
            y += 0.1  # Increase Y position to simulate increasing view height
        if keys[K_i]:
            y -= 0.1  # Decrease Y position to simulate decreasing view height

        elapsed_time += clock.get_time() / 1000.0  # Add elapsed time in seconds

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_walls()

        # Update the depth positions
        rectangle_z -= rectangle_speed

        # Start left and right rectangles after delay
        if elapsed_time >= left_start_delay:
            left_rectangle_z -= rectangle_speed
        if elapsed_time >= right_start_delay:
            right_rectangle_z -= rectangle_speed

        # Draw the rectangles with specific height and depth
        draw_rectangle(0.0, y, rectangle_z, width=1.0, height=height, depth=depth)
        draw_rectangle(left_rectangle_x, y, left_rectangle_z, width=1.0, height=height, depth=depth)
        draw_rectangle(right_rectangle_x, y, right_rectangle_z, width=1.0, height=height, depth=depth)

        # Reset the rectangles when they go too far
        if rectangle_z < -20.0:
            rectangle_z = 0.0  # Reset depth position
        if left_rectangle_z < -20.0:
            left_rectangle_z = -5.0
        if right_rectangle_z < -20.0:
            right_rectangle_z = -5.0

        # Render the parameter text on the OpenGL window
        render_text(f"Speed: {rectangle_speed:.2f}", 10, 10, pygame.display.get_surface(), font)
        render_text(f"Height: {height:.2f}", 10, 50, pygame.display.get_surface(), font)
        render_text(f"Depth: {depth:.2f}", 10, 90, pygame.display.get_surface(), font)

        pygame.display.flip()  # Update the OpenGL window

        clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    main()
