import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Union, Callable

import imgui
from typing_extensions import override

_WINDOWS_FOCUS_STATE = {}


class ImGuiWindowAbstract(ABC):
    """Abstract for window creation.

    Provide a flexible list of function to be executed around begin
    and end statement.
    """
    _focus_state = {}
    __FOCUS_ID_VALUE_ERROR_MSG = "_focus_id is not in _focus_state dict!"

    def __init__(self):
        global _WINDOWS_FOCUS_STATE
        self.__log = logging.getLogger(self.__class__.__name__)

        if self.__class__ is ImGuiWindowAbstract:
            raise TypeError("Can not instantiate an ImGuiWindowAbstract Class!")

        self._before_begin_functions = []
        self._after_end_functions = []
        self._after_begin_functions = []
        self._before_end_functions = []

        self._focus_id = f"focus-id-{id(self)}"  # Create a unique focus name
        _WINDOWS_FOCUS_STATE[self._focus_id] = False  # Not focused by default

        self.__log.debug(f"Initialize focus window {self._focus_id}.")

    @classmethod
    def _get_windows_focus_state(cls):
        """Get windows focus state global variable. It stocks windows focus state.
        :return: A dict with the windows focus state.
        """
        global _WINDOWS_FOCUS_STATE
        return _WINDOWS_FOCUS_STATE

    def draw(self, *args, **kwargs) -> None:
        """Draw ImGui window and execute declared function around
        begin and end statement.
        :return None.
        """
        for func in self._before_begin_functions:
            func()

        with self._begin_statement_window():

            for func in self._after_begin_functions:
                func()

            self._draw_content(*args, **kwargs)

            for func in self._before_end_functions:
                func()

        for func in self._after_end_functions:
            func()

    def focus(self):
        """Mark the main window as focused."""
        if self._focus_id not in self._get_windows_focus_state().keys():
            raise ValueError(self.__FOCUS_ID_VALUE_ERROR_MSG)

        # Remove previous focused element
        for focus_element, focus_flag in self._get_windows_focus_state().items():
            if focus_flag:
                self._get_windows_focus_state()[focus_element] = False
                self.__log.debug(f"Unfocus window {focus_element}")
                break

        self._get_windows_focus_state()[self._focus_id] = True  # Focus current element

        self.__log.debug(f"Focus window: {self._focus_id}")

    def unfocus(self):
        """Unmark this window as focused."""
        if self._focus_id not in self._get_windows_focus_state().keys():
            raise ValueError(self.__FOCUS_ID_VALUE_ERROR_MSG)

        self._get_windows_focus_state()[self._focus_id] = False  # Remove the focus element

        self.__log.debug(f"Unfocus window {self._focus_id}")

    def is_focused(self):
        """Return whether the element is focused or not.
        :return: Return True if the window is focused.
        """
        if self._focus_id not in self._get_windows_focus_state().keys():
            raise ValueError(self.__FOCUS_ID_VALUE_ERROR_MSG)

        return self._get_windows_focus_state()[self._focus_id]

    @abstractmethod
    def _begin_statement_window(self):
        """ImGui's instruction to begin a window."""
        pass

    @abstractmethod
    def _draw_content(self, *args, **kwargs):
        """Instructions to draw the main content of the window."""
        pass


class BasicWindow(ImGuiWindowAbstract):
    """
    Basic window with imgui.begin() statement. Used for basic many basic windows.
    """

    def __init__(self,
                 window_name: str,
                 closeable: Union[bool, None] = False,
                 imgui_window_flags: Union[int, None] = 0):
        """
        :param window_name: The title of window 
        :param closeable:
        :param imgui_window_flags:
        """
        super().__init__()

        self._window_name = window_name
        self._closeable = closeable
        self._imgui_window_flags = imgui_window_flags

    @override
    def _begin_statement_window(self):
        return imgui.begin(self._window_name, self._closeable, self._imgui_window_flags)

    @abstractmethod
    def _draw_content(self, *args, **kwargs):
        pass


# -- Menu bar --
#
# Utils for menu bar creation.

def _undefined_action():
    raise NotImplementedError("Undefined action. Have you correctly provide an action in the MenuItem?")


@dataclass
class MenuItem:
    name: Union[str, list[str]]  # It can be a list of names to dynamically change them.
    action: Callable[[], None] = _undefined_action
    selected_name: int = 0
    shortcut: str = ""
    selected: bool = False
    enabled: bool = True


@dataclass
class MenuBar:
    name: str
    menu_items: list[MenuItem] = field(default_factory=list)
    enabled: bool = True


class MenuBarWindow(ImGuiWindowAbstract):

    def __init__(self, menu_bars: Union[list[MenuBar], None] = None):
        super().__init__()

        if menu_bars is None:
            menu_bars = []
        self._menu_bars = menu_bars

    @override
    def _begin_statement_window(self):
        return imgui.begin_main_menu_bar()

    @override
    def _draw_content(self) -> None:
        """Draw menu bar

        Iterate over _menu_bars list and over menu_items list inside of it.
        For each element, display a menu_item.
        """
        for menu_bar in self._menu_bars:
            with imgui.begin_menu(menu_bar.name, menu_bar.enabled):
                for menu_item in menu_bar.menu_items:

                    if isinstance(menu_item.name, str):
                        menu_name = menu_item.name

                    elif (isinstance(menu_item.name, list)
                          and all(isinstance(name, str) for name in menu_item.name)):

                        menu_name = menu_item.name[menu_item.selected_name]

                    else:
                        raise TypeError("Invalid menu item name type!")

                    clicked, _ = imgui.menu_item(menu_name,
                                                 menu_item.shortcut,
                                                 menu_item.selected,
                                                 menu_item.enabled)

                    if clicked:
                        menu_item.action()
