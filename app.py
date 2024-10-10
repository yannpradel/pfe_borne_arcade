import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

height = 0.6
depth = 3.0
y = -3.5  # Position en bas de l'écran (Y)

# Position initiale des rectangles
rectangle_z = 0.0    # Position de profondeur du rectangle central
rectangle_speed = 0.1  # Vitesse de changement de profondeur
height = 1.8  # Hauteur du rectangle central
depth = 1.0    # Profondeur du rectangle central

# Positions pour les rectangles de gauche et droite
left_rectangle_z = -5.0    # Position de profondeur du rectangle de gauche (commence plus loin)
left_rectangle_x = -3.0   # Position X pour le rectangle de gauche
height = 1.8  # Hauteur du rectangle de gauche
depth = 1.0    # Profondeur du rectangle de gauche

right_rectangle_z = -5.0    # Position de profondeur du rectangle de droite (commence plus loin)
right_rectangle_x = 3.0    # Position X pour le rectangle de droite
height = 0.8  # Hauteur du rectangle de droite
depth = 2.0    # Profondeur du rectangle de droite

# Délai pour le démarrage des rectangles de gauche et droite
left_start_delay = 3.0  # Délai avant que le rectangle de gauche ne commence à bouger
right_start_delay = 2.0  # Délai avant que le rectangle de droite ne commence à bouger

def draw_rectangle(x, y, z, width=1.0, height=0.5, depth=1.0):
    """Dessine un rectangle 3D avec une position x, y, z spécifiées, largeur, hauteur et profondeur."""
    glBegin(GL_QUADS)

    # Dessiner la face avant
    glColor3f(0.4, 0.8, 0.4)  # Couleur grise pour la face avant
    glVertex3f(x - width, y, z + depth)  # Coin inférieur gauche
    glVertex3f(x + width, y, z + depth)  # Coin inférieur droit
    glVertex3f(x + width, y + height, z + depth)  # Coin supérieur droit
    glVertex3f(x - width, y + height, z + depth)  # Coin supérieur gauche

    # Dessiner la face arrière
    glColor3f(0.4, 0.8, 0.4)  # Couleur légèrement plus sombre pour la face arrière
    glVertex3f(x - width, y, z - depth)  # Coin inférieur gauche
    glVertex3f(x - width, y + height, z - depth)  # Coin supérieur gauche
    glVertex3f(x + width, y + height, z - depth)  # Coin supérieur droit
    glVertex3f(x + width, y, z - depth)  # Coin inférieur droit

    # Dessiner la face inférieure
    glColor3f(0.4, 0.8, 0.4)  # Couleur encore plus sombre pour la face inférieure
    glVertex3f(x - width, y, z - depth)  # Coin inférieur gauche
    glVertex3f(x + width, y, z - depth)  # Coin inférieur droit
    glVertex3f(x + width, y, z + depth)  # Coin inférieur droit
    glVertex3f(x - width, y, z + depth)  # Coin inférieur gauche

    # Dessiner la face supérieure
    glColor3f(0.4, 0.8, 0.4)  # Couleur légèrement plus claire pour la face supérieure
    glVertex3f(x - width, y + height, z + depth)  # Coin supérieur gauche
    glVertex3f(x + width, y + height, z + depth)  # Coin supérieur droit
    glVertex3f(x + width, y + height, z - depth)  # Coin supérieur droit
    glVertex3f(x - width, y + height, z - depth)  # Coin supérieur gauche

    # Dessiner les faces latérales
    glColor3f(0.5, 0.1, 0.5)  # Couleur grise pour les faces latérales
    glVertex3f(x + width, y, z + depth)  # Coin inférieur droit
    glVertex3f(x + width, y + height, z + depth)  # Coin supérieur droit
    glVertex3f(x + width, y + height, z - depth)  # Coin supérieur droit
    glVertex3f(x + width, y, z - depth)  # Coin inférieur droit

    glVertex3f(x - width, y, z + depth)  # Coin inférieur gauche
    glVertex3f(x - width, y, z - depth)  # Coin inférieur gauche
    glVertex3f(x - width, y + height, z - depth)  # Coin supérieur gauche
    glVertex3f(x - width, y + height, z + depth)  # Coin supérieur gauche

    glEnd()

def main():
    """Fonction principale du programme."""
    global rectangle_z, left_rectangle_z, right_rectangle_z

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Perspective
    glTranslatef(0.0, 0.0, -5)  # Position de la caméra

    clock = pygame.time.Clock()

    # Temps écoulé pour le démarrage des rectangles
    elapsed_time = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        elapsed_time += clock.get_time() / 1000.0  # Ajouter le temps écoulé en secondes

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Mettre à jour la profondeur des rectangles
        rectangle_z -= rectangle_speed  # Avancer légèrement en profondeur

        # Démarrer les rectangles de gauche et droite après le délai
        if elapsed_time >= left_start_delay:
            left_rectangle_z -= rectangle_speed  # Avancer le rectangle de gauche

        if elapsed_time >= right_start_delay:
            right_rectangle_z -= rectangle_speed  # Avancer le rectangle de droite

        # Dessiner les rectangles avec des hauteurs et profondeurs spécifiques
        draw_rectangle(0.0, y, rectangle_z, width=1.0, height=height, depth=depth)  # Rectangle central
        draw_rectangle(left_rectangle_x, y, left_rectangle_z, width=1.0, height=height, depth=depth)  # Rectangle de gauche
        draw_rectangle(right_rectangle_x, y, right_rectangle_z, width=1.0, height=height, depth=depth)  # Rectangle de droite

        # Limite de profondeur pour les rectangles
        if rectangle_z < -20.0:  
            rectangle_z = 0.0  # Réinitialiser la profondeur du rectangle central

        if left_rectangle_z < -20.0:
            left_rectangle_z = -5.0  # Réinitialiser la profondeur du rectangle de gauche

        if right_rectangle_z < -20.0:
            right_rectangle_z = -5.0  # Réinitialiser la profondeur du rectangle de droite

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
