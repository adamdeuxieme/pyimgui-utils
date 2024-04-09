"""A set of windows that have a custom style applied when they are focused.

This is an example on how the module can be used to keep track of the focused
windows. It uses this knowledge to adapt imgui's style values to create a
custom focus style.
"""
from __future__ import annotations

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Callable, Optional

import OpenGL.GL as gl
import imgui
import pygame

from examples.utils import setup_imgui_context
from pyimgui_utils import BasicWindow


# ------------------------------------------------------------------------------
# Utils
# ------------------------------------------------------------------------------

class Singleton(type):
    """A Singleton metaclass.

    It allows us to create singleton.
    The code come from a response on Stackoverflow.
    https://stackoverflow.com/questions/6760685/
    """
    _insts = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._insts:
            cls._insts[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._insts[cls]


class IdentifiableIT(ABC):
    """Identifiable interface.

    Object that have an identifier under get_id. It is meant to be unique,
    but no mechanism check that in this interface.
    """

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass


# ------------------------------------------------------------------------------
# Focus functions/decorators
# ------------------------------------------------------------------------------

def push_focus_style():
    """Push style colors associated with focusing a window."""
    imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 1, 1, 1, .5)


def pop_focus_style():
    """Pop style colors pushed by push_focus_style function above."""
    imgui.pop_style_color()


def update_focus_state(window: IdentifiableIT) -> None:
    """Update application state focus id.

    Should be called inside a 'begin' loop of a window to update
    application state.
    """
    if imgui.is_window_focused():
        application_state = ApplicationState.get_instance()
        application_state.set_focus_window(window)


def update_focus_state_end_loop() -> None:
    """Update the application state at the end of a loop.

    Cover the case where no windows are focused. If it's the case, reflect
    this state in application state.
    """
    if not imgui.is_window_focused(imgui.FOCUS_ANY_WINDOW):
        application_state = ApplicationState.get_instance()
        application_state.remove_focus_window()


def track_focus(cls):
    """Decorator to enable focus tracking of window instances.

    This decorator add update_focus_state function to the queue
    after_begin_functions of each instance.
    """
    old__init__ = cls.__init__

    def new__init__(*args, **kwargs):
        old__init__(*args, **kwargs)
        self = args[0]
        self.after_begin_functions.append(
            lambda: update_focus_state(self)
        )

    new__init__.__doc__ = old__init__.__doc__
    cls.__init__ = new__init__

    return cls


# ------------------------------------------------------------------------------
# Custom windows
# ------------------------------------------------------------------------------


class BasicWindowWithId(BasicWindow, IdentifiableIT):
    """Extend BasicWindow class with an identifier under get_id."""

    def get_id(self) -> str:
        return str(id(self))

    @abstractmethod
    def draw_content(self, *args, **kwargs):
        pass


@track_focus
class DummyWindow(BasicWindowWithId):
    """Very basic window."""

    def draw_content(self, *args, **kwargs):
        imgui.text("Hello World!")


# ------------------------------------------------------------------------------
# Application State
# ------------------------------------------------------------------------------

@dataclass
class State:
    focus_window_id: str = ""


class ApplicationState(metaclass=Singleton):
    _inst = None

    def __init__(self):
        self.state = State()
        self._set_instance(self)

    @classmethod
    def get_instance(cls) -> ApplicationState:
        return cls._inst

    @classmethod
    def _set_instance(cls, instance: ApplicationState) -> None:
        cls._inst = instance

    @property
    def focus_window_id(self) -> str:
        return self.state.focus_window_id

    def set_focus_window(self, window: IdentifiableIT):
        self.state.focus_window_id = window.get_id()

    def remove_focus_window(self):
        self.state.focus_window_id = ""


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------

def main():
    app_state = ApplicationState()

    wnds = [DummyWindow(name=f"Window {i}")
            for i in range(5)]

    impl = setup_imgui_context()

    should_stop_flag = False
    while not should_stop_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_stop_flag = True
            impl.process_event(event)
        impl.process_inputs()
        imgui.new_frame()

        for wnd in wnds:
            is_wnd_focus = (wnd.get_id() == app_state.focus_window_id)
            if is_wnd_focus:
                push_focus_style()

            wnd.draw()

            if is_wnd_focus:
                pop_focus_style()

        gl.glClearColor(0.1, 0.2, 0.2, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        update_focus_state_end_loop()
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()

    impl.shutdown()


if __name__ == "__main__":
    main()
