"""A window with a digit displays

Just a window with the same digit layout them old phones.

The purpose is to present a use-case where it can be
"""
import OpenGL.GL as gl
import imgui
import pygame

from examples.utils import setup_imgui_context
from pyimgui_utils import BasicWindow, Button


class DigitWindow(BasicWindow):

    def __init__(self):
        """Digit window

        The purpose is to mock an old phone where you would have to type
        a number and call someone.

        It uses list comprehensions to creates the lines of buttons.
        The call button uses the hold feature of Button to display a different
        color when you can't perform a call (no number typed).
        """
        flags = imgui.WINDOW_ALWAYS_AUTO_RESIZE
        super().__init__(
            name="Digit Window",
            imgui_window_flags=flags
        )
        self.typed_input = ""
        self.line1 = [Button(label=f"{i}",
                             btn_callback=lambda x=i: self._type_char(f"{x}"))
                      for i in range(1, 4)]
        self.line2 = [Button(label=f"{i}",
                             btn_callback=lambda x=i: self._type_char(f"{x}"))
                      for i in range(4, 7)]
        self.line3 = [Button(label=f"{i}",
                             btn_callback=lambda x=i: self._type_char(f"{x}"))
                      for i in range(7, 10)]
        self.line4 = [Button(label="*",
                             btn_callback=lambda: self._type_char("*")),
                      Button(label="0",
                             btn_callback=lambda: self._type_char("0")),
                      Button(label="#",
                             btn_callback=lambda: self._type_char("#"))]
        self.lines = [self.line1, self.line2, self.line3, self.line4]
        self.call_btn = Button(
            label="Call",
            btn_callback=self._call,
            btn_color=(0.0, 1.0, 0.0),  # Green
            hold_btn_color=(0.2, 0.2, 0.2),  # Grey, because you can't call
            hold_condition=lambda: len(self.typed_input) == 0
        )

    def _type_char(self, char: str):
        """Type a character in the window

        Append the typed_input attribute of this window.
        :param char: The character to add to the input attribute.
        """
        self.typed_input += char

    def _call(self):
        """Mock a call

        Reset the typed_input attribute of this window,
        """
        self.typed_input = ""

    def draw_content(self, *args, **kwargs) -> None:
        imgui.text(f"{self.typed_input = }")
        for ln in self.lines:
            list(map(lambda e: {e.draw(), imgui.same_line()}, ln))
            imgui.new_line()
        self.call_btn.draw()


def main():
    impl = setup_imgui_context()
    digit_window = DigitWindow()

    should_stop_flag = False
    while not should_stop_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_stop_flag = True
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()

        digit_window.draw()

        gl.glClearColor(0.1, 0.2, 0.2, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()

    impl.shutdown()


if __name__ == "__main__":
    main()
