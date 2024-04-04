from typing import Any, Tuple

import OpenGL.GL as gl
import imgui
import numpy as np
import pygame
from glfw.GLFW import glfwTerminate
from imgui.integrations.glfw import GlfwRenderer
from imgui.integrations.pygame import PygameRenderer


def setup_imgui_context() -> [GlfwRenderer, Any, Any]:
    pygame.init()
    size = 800, 600

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size
    io.ini_file_name = None
    return impl


def terminate_imgui_context(impl, ctx) -> None:
    impl.shutdown()
    glfwTerminate()
    imgui.destroy_context(ctx)


def draw_square(position, color: Tuple[int, int, int] = None):
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
    gl.glEnd()  # We are done drawing the polygon
