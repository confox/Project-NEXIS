import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
import time

# Define vibrant purple shades for transitions
PURPLE_SHADES = [
    np.array([0.8, 0.2, 1.0]),  # Vibrant Purple
    np.array([0.9, 0.6, 1.0]),  # Light Vibrant Purple
    np.array([0.6, 0.0, 0.8]),  # Dark Vibrant Purple
]

# Interpolate between two colors
def interpolate_color(color1, color2, t):
    return color1 * (1 - t) + color2 * t

# Initialize particle system
def generate_particles(num_particles=10000):
    particles = []
    for _ in range(num_particles):
        phi = random.uniform(0, 2 * np.pi)
        theta = random.uniform(0, np.pi)
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        particles.append([x, y, z])
    return particles

def generate_floating_particles(num_particles=5000):
    floating_particles = []
    for _ in range(num_particles):
        x, y, z = np.random.uniform(-3, 3, 3)
        floating_particles.append([x, y, z])
    return floating_particles

def draw_particles(particles, color):
    glBegin(GL_POINTS)
    glColor3f(*color)
    for p in particles:
        glVertex3f(p[0], p[1], p[2])
    glEnd()

def draw_floating_particles(particles, color):
    glBegin(GL_POINTS)
    for p in particles:
        color = np.random.rand(3)
        glColor3f(*color)
        glVertex3f(p[0], p[1], p[2])
    glEnd()

# Initialize lighting and material properties
def init_lighting_and_material():
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    # Light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])
    glEnable(GL_LIGHT0)

    # Light 1
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT1, GL_POSITION, [-5, -5, 5, 1])
    glEnable(GL_LIGHT1)

# Main loop
def main():
    pygame.init()

    screen_size = (800, 600)
    display = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL | RESIZABLE | SRCALPHA)
    gluPerspective(45, screen_size[0] / screen_size[1], 0.1, 50)
    glTranslate(0, 0, -5)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    init_lighting_and_material()

    clock = pygame.time.Clock()

    start_time = time.time()
    color_index = 1
    transition_time = 4  # seconds

    particles = generate_particles()
    floating_particles = generate_floating_particles()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(45, event.w / event.h, 0.1, 50)
                glMatrixMode(GL_MODELVIEW)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 0.0)  # Transparent background

        # Color transition
        elapsed_time = time.time() - start_time
        t = (elapsed_time % transition_time) / transition_time
        next_color_index = (color_index + 1) % len(PURPLE_SHADES)
        current_color = interpolate_color(PURPLE_SHADES[color_index], PURPLE_SHADES[next_color_index], t)
        if elapsed_time > transition_time:
            start_time = time.time()
            color_index = next_color_index

        # Rotate and draw particles
        glPushMatrix()
        glRotatef(elapsed_time * 20, 1, 1, 0)
        draw_particles(particles, current_color)
        glPopMatrix()

        # Draw floating particles
        glPushMatrix()
        glRotatef(elapsed_time * 10, 0, 1, 0)
        draw_floating_particles(floating_particles, current_color)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
