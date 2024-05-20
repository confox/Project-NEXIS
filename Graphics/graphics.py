import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time

# Define colors for transitions
COLORS = [
    np.array([1.0, 0.0, 0.0]),  # Red
    np.array([0.5, 0.0, 0.5]),  # Purple
    np.array([0.0, 0.0, 1.0])   # Blue
]

# Interpolate between two colors
def interpolate_color(color1, color2, t):
    return color1 * (1 - t) + color2 * t

# Draw sphere
def draw_sphere(radius=1.0, slices=40, stacks=40):
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
    glEnable(GL_LIGHT0)

    # Light 1
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT1, GL_POSITION, [-1, -1, -1, 0])
    glEnable(GL_LIGHT1)

# Initialize material properties
def init_material():
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

# Mouse control for interactive rotation and zoom
rotation_speed = 0.5
zoom_speed = 0.1
current_angle = [0, 0]

def handle_mouse():
    global current_angle
    mouse_state = pygame.mouse.get_pressed()
    mouse_rel = pygame.mouse.get_rel()

    if mouse_state[0]:
        current_angle[0] += mouse_rel[1] * rotation_speed
        current_angle[1] += mouse_rel[0] * rotation_speed

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        glTranslatef(0, 0, zoom_speed)
    if keys[K_DOWN]:
        glTranslatef(0, 0, -zoom_speed)

# GLSL Shaders
vertex_shader_source = """
#version 130
in vec4 position;
in vec3 normal;
out vec3 frag_normal;
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * position;
    frag_normal = normal;
}
"""

fragment_shader_source = """
#version 130
in vec3 frag_normal;
out vec4 frag_color;
uniform vec3 light_color;
void main() {
    float intensity = max(dot(normalize(frag_normal), vec3(0, 0, 1)), 0.0);
    frag_color = vec4(light_color * intensity, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def init_shaders():
    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(shader_program))
    glUseProgram(shader_program)
    return shader_program

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    init_lighting()
    init_material()

    shader_program = init_shaders()
    light_color_location = glGetUniformLocation(shader_program, "light_color")

    clock = pygame.time.Clock()

    start_time = time.time()
    color_index = 0

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        handle_mouse()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Color transition
        elapsed_time = time.time() - start_time
        t = (elapsed_time % 2) / 2.0
        next_color_index = (color_index + 1) % len(COLORS)
        current_color = interpolate_color(COLORS[color_index], COLORS[next_color_index], t)
        if elapsed_time > 2:
            start_time = time.time()
            color_index = next_color_index

        # Rotate sphere
        glPushMatrix()
        glRotatef(current_angle[0], 1, 0, 0)
        glRotatef(current_angle[1], 0, 1, 0)
        glUniform3fv(light_color_location, 1, current_color)
        draw_sphere()
        glPopMatrix()

        pygame.display.flip()

if __name__ == "__main__":
    main()
