from typing import Any, Tuple

import OpenGL.GL as gl
import imgui
import numpy as np
import pygame
from glfw.GLFW import glfwTerminate
from imgui.integrations.glfw import GlfwRenderer
from imgui.integrations.pygame import PygameRenderer


def setup_imgui_context() -> [GlfwRenderer, Any, Any]:
    """Set up an imgui context with pygame.

    Strongly inspired from pygame integration example of pyimgui repo.
    https://github.com/pyimgui/pyimgui/blob/master/doc/examples/integrations_pygame.py
    """
    pygame.init()
    size = 800, 600

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size
    io.ini_file_name = None
    return impl


def draw_square(position, color: Tuple[int, int, int] = None):
    """Draw a square on the screen

    Note that a position of [0.0, 0.0] refers to the center of the screen,
    a position of [1.0, 1.0] refers to the top right corner of the screen etc.

    :param position: A position Tuple.
    :param color: A Tuple of three int representing RGB values between 0 and 255
    """
    square = np.array([[-0.2, -0.2],
                       [0.2, -0.2],
                       [0.2, 0.2],
                       [-0.2, 0.2]])

    if color is not None:
        gl.glColor3f(*color)

    square_position = [[sq[0] + position[0], sq[1] + position[1]] for sq in square]
    gl.glBegin(gl.GL_QUADS)  # Start drawing a 4 sided polygon
    gl.glVertex2f(*square_position[0])  # Bottom Left
    gl.glVertex2f(*square_position[1])  # Bottom Right
    gl.glVertex2f(*square_position[2])  # Top Right
    gl.glVertex2f(*square_position[3])  # Top Left
    gl.glEnd()
