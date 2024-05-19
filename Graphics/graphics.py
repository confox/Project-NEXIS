#!/usr/bin/env python
import pygame
import pygame_gui
import psutil
import random
import math
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame and GUI manager
pygame.init()
pygame.display.set_caption("Advanced JARVIS Visualization")
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)
manager = pygame_gui.UIManager((800, 600))

# Create GUI elements
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 550), (100, 50)),
                                            text='Start',
                                            manager=manager)

# Initialize OpenGL
glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)

def draw_3d_rotating_cube(angle):
    glPushMatrix()
    glRotatef(angle, 1, 1, 0)
    glBegin(GL_QUADS)

    # Front face
    glColor3f(0, 1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    # Back face
    glColor3f(0, 1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, -1, -1)

    # Top face
    glColor3f(0, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)

    # Bottom face
    glColor3f(0, 1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)

    # Right face
    glColor3f(0, 1, 1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)

    # Left face
    glColor3f(0, 1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)

    glEnd()
    glPopMatrix()

def draw_particles(particles):
    for p in particles:
        p['x'] += p['speed'] * math.cos(p['angle'])
        p['y'] += p['speed'] * math.sin(p['angle'])
        if p['x'] < 0 or p['x'] > 800 or p['y'] < 0 or p['y'] > 600:
            p['x'], p['y'] = 400, 300
            p['angle'] = random.uniform(0, 2 * math.pi)
        pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), int(p['size']))

def draw_system_info(font):
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    net_io = psutil.net_io_counters()

    cpu_text = font.render(f"CPU Usage: {cpu_percent}%", True, (0, 255, 255))
    mem_text = font.render(f"Memory Usage: {memory_info.percent}%", True, (0, 255, 255))
    net_text = font.render(f"Net Sent: {net_io.bytes_sent / (1024 * 1024):.2f} MB, Recv: {net_io.bytes_recv / (1024 * 1024):.2f} MB", True, (0, 255, 255))

    screen.blit(cpu_text, (10, 10))
    screen.blit(mem_text, (10, 40))
    screen.blit(net_text, (10, 70))

# Main loop
running = True
clock = pygame.time.Clock()
angle = 0
particles = [{'x': random.uniform(0, 800), 'y': random.uniform(0, 600), 'size': random.uniform(2, 5), 'speed': random.uniform(1, 3), 'angle': random.uniform(0, 2 * math.pi), 'color': (0, 255, random.randint(100, 255))} for _ in range(50)]
font = pygame.font.SysFont("Helvetica", 24)

while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

    manager.update(time_delta)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw 3D cube
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    draw_3d_rotating_cube(angle)
    angle += 1

    pygame.display.flip()

    # Draw 2D HUD elements
    screen.fill((0, 0, 0))

    # Draw particles
    draw_particles(particles)

    # Draw static lines and text
    pygame.draw.line(screen, (0, 255, 255), (0, 300), (350, 300), 2)
    pygame.draw.line(screen, (0, 255, 255), (450, 300), (800, 300), 2)

    jarvis_text = font.render("JARVIS", True, (0, 255, 255))
    system_online_text = font.render("System Online", True, (0, 255, 255))
    screen.blit(jarvis_text, (400 - jarvis_text.get_width() // 2, 50))
    screen.blit(system_online_text, (400 - system_online_text.get_width() // 2, 550))

    # Draw system info
    draw_system_info(font)

    # Draw GUI elements
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
