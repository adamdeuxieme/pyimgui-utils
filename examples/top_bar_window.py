"""A Dummy window with a top bar

In this example, you can read how pyimgui_utils is used to create a dummy
window with a top bar.

The dummy only contains text. The top bar contains the window title and 3
buttons. The red one close the window. The 2 other only print their color.

There is a menu bar that allow user to show to dummy window if it has been
closed.

To spice things up, the buttons mock the style of the 'fruit trade' ones.
"""
from typing import Callable

import OpenGL.GL as gl
import imgui
import pygame

from examples.utils import setup_imgui_context
from pyimgui_utils import BasicWindow, Button
from pyimgui_utils.interface import DrawableIT
from pyimgui_utils.window import (WindowStack, WindowStackOrientation, MenuBar,
                                  MenuItem, MenuBarWindow)


class DummyWindow(BasicWindow):

    def __init__(self):
        super().__init__(
            name="Dummy window",
            imgui_window_flags=imgui.WINDOW_NO_TITLE_BAR
        )
        self.size = (0.0, 0.0)
        self.before_end_functions.append(
            lambda: self._update_size(imgui.get_window_size())
        )

    def draw_content(self, *args, **kwargs) -> None:
        for _ in range(5):
            imgui.text("Dummy window")

    def _update_size(self, size):
        self.size = size


class TopBarWindow(BasicWindow):

    def __init__(self,
                 title: str,
                 red_btn_function: Callable[[], None]):
        flags = (imgui.WINDOW_NO_TITLE_BAR
                 | imgui.WINDOW_NO_RESIZE
                 | imgui.WINDOW_NO_SCROLLBAR)
        super().__init__(name="Top bar",
                         imgui_window_flags=flags)

        # Adjust style
        button_size = 12
        self.before_begin_functions.append(
            lambda: imgui.push_style_var(
                imgui.STYLE_WINDOW_BORDERSIZE, 0.0
            )
        )
        self.before_begin_functions.append(
            lambda: imgui.push_style_var(
                imgui.STYLE_ITEM_SPACING, (5.0, 0.0)
            )
        )
        self.before_begin_functions.append(
            lambda: imgui.push_style_var(
                imgui.STYLE_FRAME_PADDING, (0.0, 0.0)
            )
        )
        self.before_begin_functions.append(
            lambda: imgui.push_style_var(
                imgui.STYLE_FRAME_ROUNDING,
                button_size / 2
            )
        )
        self.after_end_functions.append(
            lambda: imgui.pop_style_var(4)
        )

        # Define 3 buttons
        self.green_btn = Button("",
                                btn_callback=lambda: print("Green btn pressed"),
                                btn_color=(0.0, 0.5, 0.0),
                                btn_color_hovered=(0.0, 0.7, 0.0),
                                btn_color_active=(0.0, 0.9, 0.0),
                                width=button_size,
                                height=button_size)
        self.red_btn = Button("",
                              btn_callback=red_btn_function,
                              btn_color=(0.5, 0.0, 0.0),
                              btn_color_hovered=(0.7, 0.0, 0.0),
                              btn_color_active=(0.9, 0.0, 0.0),
                              width=button_size,
                              height=button_size
                              )
        self.orange_btn = Button("",
                                 btn_callback=lambda: print("Orange btn pressed"),
                                 btn_color=(0.5, 0.5, 0.0),
                                 btn_color_hovered=(0.7, 0.7, 0.0),
                                 btn_color_active=(0.9, 0.9, 0.0),
                                 width=button_size,
                                 height=button_size
                                 )

        # Update size
        self.size = (0.0, 0.0)
        self.before_end_functions.append(
            lambda: self._update_size(imgui.get_window_size())
        )

        # Title
        self.title = title

    def draw_content(self, *args, **kwargs) -> None:
        button_vertical_offset = 2
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + button_vertical_offset)
        self.red_btn.draw()
        imgui.same_line()
        self.orange_btn.draw()
        imgui.same_line()
        self.green_btn.draw()
        imgui.same_line()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - button_vertical_offset)
        imgui.text(self.title)

    def _update_size(self, size):
        self.size = size


class DummyWindowWithTopBar(DrawableIT):

    def __init__(self, close_function: Callable[[], None]):
        self.dummy_window = DummyWindow()
        self.top_bar = TopBarWindow(
            "Dummy window",
            red_btn_function=close_function
        )
        self.top_bar.before_begin_functions.append(
            lambda: imgui.set_next_window_size(
                self.dummy_window.size[0],
                self.top_bar.size[1]
            )
        )
        self.wnd_hstack = WindowStack(
            wnds=[self.top_bar, self.dummy_window],
            orientation=WindowStackOrientation.VERTICAL,
            offset=0
        )

    def draw(self, *args, **kwargs) -> None:
        self.wnd_hstack.draw()


def main():
    impl = setup_imgui_context()

    # Create the SquarePositionWindow
    dummy_window_opened_flag = True

    open_dummy_window = MenuItem(name="Open dummy window")
    open_dummy_window.enabled = not dummy_window_opened_flag

    def show_dummy_window():
        nonlocal dummy_window_opened_flag
        dummy_window_opened_flag = True
        open_dummy_window.enabled = False

    def hide_dummy_window():
        nonlocal dummy_window_opened_flag
        dummy_window_opened_flag = False
        open_dummy_window.enabled = True

    open_dummy_window.action = show_dummy_window

    menu_bar = MenuBar(name="View", menu_items=[open_dummy_window])
    menu_bar_window = MenuBarWindow(menu_bars=[menu_bar])

    dummy_window_with_top_bar = DummyWindowWithTopBar(
        close_function=hide_dummy_window
    )

    should_stop_flag = False
    while not should_stop_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_stop_flag = True
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()
        menu_bar_window.draw()
        if dummy_window_opened_flag:
            dummy_window_with_top_bar.draw()

        gl.glClearColor(0.3, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()

    impl.shutdown()


if __name__ == "__main__":
    main()
