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

def interpolate_color(color1, color2, t):
    """Interpolate between two colors."""
    return color1 * (1 - t) + color2 * t

class ParticleSystem:
    def __init__(self, num_particles=10000):
        self.particles = self.generate_particles(num_particles)
        self.floating_particles = self.generate_floating_particles(num_particles // 2)

    def generate_particles(self, num_particles):
        particles = []
        for _ in range(num_particles):
            phi = random.uniform(0, 2 * np.pi)
            theta = random.uniform(0, np.pi)
            x = np.sin(theta) * np.cos(phi)
            y = np.sin(theta) * np.sin(phi)
            z = np.cos(theta)
            particles.append([x, y, z])
        return particles

    def generate_floating_particles(self, num_particles):
        floating_particles = []
        for _ in range(num_particles):
            x, y, z = np.random.uniform(-3, 3, 3)
            floating_particles.append([x, y, z])
        return floating_particles

    def draw_particles(self, particles, color):
        glBegin(GL_POINTS)
        glColor3f(*color)
        for p in particles:
            glVertex3f(p[0], p[1], p[2])
        glEnd()

    def draw_floating_particles(self, particles):
        glBegin(GL_POINTS)
        for p in particles:
            color = np.random.rand(3)
            glColor3f(*color)
            glVertex3f(p[0], p[1], p[2])
        glEnd()

class Lighting:
    def __init__(self):
        self.setup_lighting()

    def setup_lighting(self):
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

class TimeManager:
    def __init__(self, transition_time=4):
        self.start_time = time.time()
        self.color_index = 0
        self.transition_time = transition_time

    def update_color(self, shades):
        elapsed_time = time.time() - self.start_time
        t = (elapsed_time % self.transition_time) / self.transition_time
        next_color_index = (self.color_index + 1) % len(shades)
        current_color = interpolate_color(shades[self.color_index], shades[next_color_index], t)
        if elapsed_time > self.transition_time:
            self.start_time = time.time()
            self.color_index = next_color_index
        return current_color

def main():
    pygame.init()

    screen_size = (800, 600)
    display = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL | RESIZABLE | SRCALPHA)
    gluPerspective(45, screen_size[0] / screen_size[1], 0.1, 50)
    glTranslate(0, 0, -5)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    lighting = Lighting()
    time_manager = TimeManager()
    particle_system = ParticleSystem()

    clock = pygame.time.Clock()

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

        current_color = time_manager.update_color(PURPLE_SHADES)

        glPushMatrix()
        elapsed_time = time.time() - time_manager.start_time
        glRotatef(elapsed_time * 20, 1, 1, 0)
        particle_system.draw_particles(particle_system.particles, current_color)
        glPopMatrix()

        glPushMatrix()
        glRotatef(elapsed_time * 10, 0, 1, 0)
        particle_system.draw_floating_particles(particle_system.floating_particles)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
