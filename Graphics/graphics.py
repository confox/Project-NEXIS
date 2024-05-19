import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define colors
RED = (1.0, 0.0, 0.0)
PURPLE = (0.5, 0.0, 0.5)
BLUE = (0.0, 0.0, 1.0)

# Draw sphere
def draw_sphere(radius=1.0, slices=30, stacks=30):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)

# Initialize lighting
def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    # Light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])

    # Light 1
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT1, GL_POSITION, [-1, -1, -1, 0])

# Initialize material properties
def init_material():
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

# Mouse control for interactive rotation and zoom
def mouse_control():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                glTranslatef(0, 0, 1)
            elif event.button == 5:
                glTranslatef(0, 0, -1)
            elif event.button == 1:
                x, y = event.pos
                width, height = pygame.display.get_surface().get_size()
                normalized_x = (2.0 * x - width) / width
                normalized_y = (height - 2.0 * y) / height
                glRotatef(30 * normalized_x, 0, 1, 0)
                glRotatef(30 * normalized_y, 1, 0, 0)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    init_lighting()
    init_material()

    while True:
        mouse_control()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw spheres with different colors
        glColor3fv(RED)
        draw_sphere()

        glTranslatef(3, 0, 0)
        glColor3fv(PURPLE)
        draw_sphere()

        glTranslatef(-6, 0, 0)
        glColor3fv(BLUE)
        draw_sphere()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
