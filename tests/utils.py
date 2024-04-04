from typing import Any

import glfw
from glfw.GLFW import glfwTerminate
from OpenGL.GL import GL_TRUE
import imgui
from imgui.integrations.glfw import GlfwRenderer

from pyimgui_utils import BasicWindow


def setup_imgui_context() -> [GlfwRenderer, Any, Any]:
    """Setup imgui context

    Strongly inspired from the tests in pyimgui repo.
    Repo link: https://github.com/pyimgui/pyimgui/
    """

    width, height = 800, 400
    window_name = "TestImGuiWindowAbstract"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        width, height, window_name, None, None
    )

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    glfw.make_context_current(window)

    ctx = imgui.create_context()
    impl = GlfwRenderer(window)
    impl.io.ini_file_name = None
    return impl, window, ctx


def terminate_imgui_context(impl, ctx) -> None:
    impl.shutdown()
    glfwTerminate()
    imgui.destroy_context(ctx)


class DummyWindow(BasicWindow):

    def __init__(self):
        super().__init__(
            name=f"{id(self)}"
        )

    def draw_content(self, *args, **kwargs) -> None:
        imgui.text("Dummy window")


class FixedSizeWindow(BasicWindow):

    def __init__(self, x: float, y: float):
        super().__init__(
            name=f"Fixed size window-{id(self)}",
            imgui_window_flags=imgui.WINDOW_NO_RESIZE
        )
        self.before_begin_functions.append(
            lambda: imgui.set_next_window_size(x, y)
        )
        self.size = (x, y)

    def draw_content(self, *args, **kwargs) -> None:
        imgui.text("Fixed size window.")
