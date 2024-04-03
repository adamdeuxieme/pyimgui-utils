import time
from typing import Union, List

import glfw
import imgui
from OpenGL.raw.GL.VERSION.GL_1_0 import glClear, GL_COLOR_BUFFER_BIT
from glfw.GLFW import (glfwPollEvents, glfwSwapBuffers)
from typing_extensions import override, Optional

from pyimgui_utils import BasicWindow, Button
from pyimgui_utils.interface import DrawableIT
from tests.utils import setup_imgui_context, terminate_imgui_context


class TestWindow(BasicWindow):
    """Context window for interactive test

    This window display the expected behavior as a description text.
    It also provides a button to click to validate a test.
    If pressed, the pytest will be considered as passed. If not,
    the test will be considered as failed.
    """

    def __init__(self,
                 expected_behavior: Union[List[str], str],
                 window_name: Optional[str] = "Test Window"):
        """Build test context window

        :param expected_behavior: Description of expected behavior. The human
                                 operator will validate this behavior.
                                 It's either a list of lines or one line.
        :param window_name: Name of the window to display.
        """
        super().__init__(window_name)
        self.test_passes = None
        self.expected_behavior = expected_behavior
        self.test_passes_btn = Button(
            label="Test passes",
            btn_callback=self.pass_factory(),
        )
        self.test_fails_btn = Button(
            label="Test fails",
            btn_callback=self.fail_test,
        )

    @override
    def draw_content(self, *args, **kwargs) -> None:
        if isinstance(self.expected_behavior, list):
            for line in self.expected_behavior:
                imgui.text(line)

        elif isinstance(self.expected_behavior, str):
            imgui.text(self.expected_behavior)

        else:
            raise TypeError("expected_behavior must be a list or str!")

        imgui.push_style_color(imgui.COLOR_BUTTON, 0., 1., 0., 1.)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0., 1., 0., 1.)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0., 1., 0., 1.)
        imgui.push_style_color(imgui.COLOR_TEXT, 0., 0., 0., 1.)
        self.test_passes_btn.draw(*args, **kwargs)
        imgui.pop_style_color(4)

        imgui.same_line()

        imgui.push_style_color(imgui.COLOR_BUTTON, 1., 0., 0., 1.)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 1., 0., 0., 1.)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 1., 0., 0., 1.)
        self.test_fails_btn.draw(*args, **kwargs)
        imgui.pop_style_color(3)

    def pass_factory(self):
        """Mark the test as passed and close the window"""

        def pass_test(window):
            self.test_passes = True
            glfw.set_window_should_close(window, True)

        return pass_test

    @staticmethod
    def fail_test(window):
        glfw.set_window_should_close(window, True)


def run_test_window(window_under_test: DrawableIT,
                    expected_behavior: Union[List[str], str]):
    tw = TestWindow(
        expected_behavior=expected_behavior
    )
    impl, window, ctx = setup_imgui_context()

    try:
        while not glfw.window_should_close(window):
            glfwPollEvents()
            impl.process_inputs()
            imgui.new_frame()

            window_under_test.draw()
            tw.draw(window)

            glClear(GL_COLOR_BUFFER_BIT)
            imgui.render()
            impl.render(imgui.get_draw_data())
            glfwSwapBuffers(window)
    finally:
        terminate_imgui_context(impl, ctx)

    if tw.test_passes is None:
        raise InteractiveTestException("The interactive test appears to have "
                                       "terminated without specifying whether "
                                       "it passes or fails. \n"
                                       "It mays happen if the operator close "
                                       "the main window without clicking on "
                                       "'Test passes' or on 'Test fails' "
                                       "buttons.")

    assert tw.test_passes, ("Expected behavior unmatch. "
                            "Expected behavior: "
                            + "".join(tw.expected_behavior)
                            .__repr__())


class InteractiveTestException(Exception):
    def __init__(self, message):
        super().__init__(message)
