import pygame
from OpenGL.raw.GLU import gluPerspective, gluNewQuadric, gluQuadricDrawStyle, GLU_FILL, gluQuadricTexture, gluSphere, \
    gluQuadricOrientation, GLU_INSIDE
from pygame.locals import *
from OpenGL.GL import *
from PIL import Image

# Initialize Pygame
pygame.init()

# Set the display dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Variables for click-and-drag interaction
mouse_dragging = False
start_mouse_pos = (0, 0)
rotation_speed = 0.2
x_rotation = 0
y_rotation = 0


def setup_perspective():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 2000.0)  # Increase far clipping plane
    glMatrixMode(GL_MODELVIEW)


def draw_earth(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    glEnable(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, earth_texture_data)
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, slices, stacks)
    glDisable(GL_TEXTURE_2D)


def draw_stars(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluQuadricOrientation(quadric, GLU_INSIDE)
    glEnable(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, stars_width, stars_height, 0, GL_RGB, GL_UNSIGNED_BYTE, stars_texture_data)
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, slices, stacks)
    glDisable(GL_TEXTURE_2D)


glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

earth_texture = Image.open("earth_texture.jpg")
earth_texture_data = earth_texture.tobytes("raw", "RGB")
width, height = earth_texture.size

stars_texture = Image.open("stars_texture.jpeg")
stars_texture_data = stars_texture.tobytes("raw", "RGB")
stars_width, stars_height = stars_texture.size

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_dragging = True
                start_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_dragging = False

    if mouse_dragging:
        current_mouse_pos = pygame.mouse.get_pos()
        dx, dy = current_mouse_pos[0] - start_mouse_pos[0], current_mouse_pos[1] - start_mouse_pos[1]
        x_rotation += dy * rotation_speed
        y_rotation += dx * rotation_speed
        start_mouse_pos = current_mouse_pos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Adjust the Z-translation to view the entire Earth
    glTranslatef(0.0, 0.0, -6)

    setup_perspective()

    glRotatef(x_rotation, 1, 0, 0)
    glRotatef(y_rotation, 0, 1, 0)

    glDisable(GL_CULL_FACE)
    draw_stars(1.5 * 1000, 32, 32)
    glEnable(GL_CULL_FACE)

    draw_earth(1.5, 32, 32)

    pygame.display.flip()
    pygame.time.wait(10)
