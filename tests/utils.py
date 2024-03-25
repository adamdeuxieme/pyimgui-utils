import glfw
from OpenGL.GL import GL_TRUE
import imgui
from imgui.integrations.glfw import GlfwRenderer

from pyimgui_utils import ImGuiWindowAbstract


def setup_imgui_context() -> GlfwRenderer:
    """Setup imgui context

    Strongly inspired form the tests from pyimgui repo.
    Repo link: https://github.com/pyimgui/pyimgui/
    """

    width, height = 300, 300
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
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    imgui.create_context()
    return GlfwRenderer(window)
