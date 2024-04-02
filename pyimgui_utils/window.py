import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Union, Callable, List

import imgui
from typing_extensions import override


class ImGuiWindowAbstract(ABC):
    """Abstract for window creation.

    Provide a flexible list of function to be executed around begin
    and end statement.
    """
    __FOCUS_ID_VALUE_ERROR_MSG = "focus_id is not in _focus_state dict!"

    # Focus state of every class children.
    # Never mutate this attribute with self reference!
    # Always use class reference. Otherwise, an instance attribute
    # while shadow the class attribute.
    window_focus_state = {}  # todo: switch for a dataclass object

    def __init__(self):
        self.__log = logging.getLogger(self.__class__.__name__)

        if self.__class__ is ImGuiWindowAbstract:
            raise TypeError("Can not instantiate an ImGuiWindowAbstract Class!")

        self.before_begin_functions = []
        self.after_end_functions = []
        self.after_begin_functions = []
        self.before_end_functions = []

        self.focus_id = f"focus-id-{id(self)}"  # Create a unique focus id
        ImGuiWindowAbstract._init_window_focus_state(self)

        self.__log.debug(f"Initialize focus window {self.focus_id}.")

    @classmethod
    def _init_window_focus_state(cls, window):
        cls.window_focus_state[window.focus_id] = False  # Not focused by default

    def draw(self, *args, **kwargs) -> None:
        """Draw ImGui window and execute declared function around
        begin and end statement.
        """
        for func in self.before_begin_functions:
            func()

        with self._begin_statement_window():

            for func in self.after_begin_functions:
                func()

            self.draw_content(*args, **kwargs)

            for func in self.before_end_functions:
                func()

        for func in self.after_end_functions:
            func()

    def focus(self):
        """Mark the main window as focused."""
        if self.focus_id not in self.window_focus_state.keys():
            raise ValueError(self.__FOCUS_ID_VALUE_ERROR_MSG)

        # Remove previous focused element
        for focus_element, focus_flag in self.window_focus_state.items():
            if focus_flag:
                self.window_focus_state[focus_element] = False
                self.__log.debug(f"Unfocus window {focus_element}")
                break

        ImGuiWindowAbstract.window_focus_state[self.focus_id] = True  # Focus current element

        self.__log.debug(f"Focus window: {self.focus_id}")

    def unfocus(self):
        """Unmark this window as focused."""
        if self.focus_id not in self.window_focus_state.keys():
            raise ValueError(self.__FOCUS_ID_VALUE_ERROR_MSG)

        ImGuiWindowAbstract.window_focus_state[self.focus_id] = False  # Remove the focus element

        self.__log.debug(f"Unfocus window {self.focus_id}")

    def is_focused(self):
        """Return whether the element is focused or not.
        :return: Return True if the window is focused.
        """
        if self.focus_id not in self.window_focus_state.keys():
            raise ValueError(self.__FOCUS_ID_VALUE_ERROR_MSG)

        return self.window_focus_state[self.focus_id]

    @abstractmethod
    def _begin_statement_window(self):
        """ImGui's instruction to begin a window.
        Use in 'with' statement to safely open and close the imgui window.
        e.g. imgui.begin('window_name')
        """
        pass

    @abstractmethod
    def draw_content(self, *args, **kwargs):
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
        """Basic window
         The most basic window opened with imgui.begin().

        :param window_name: The title of window
        :param closeable: True if the window is closeable, False otherwise
        :param imgui_window_flags: Optional imgui window flags
        """
        super().__init__()

        self._window_name = window_name
        self._closeable = closeable
        self._imgui_window_flags = imgui_window_flags

    @override
    def _begin_statement_window(self):
        return imgui.begin(self._window_name, self._closeable, self._imgui_window_flags)

    @abstractmethod
    def draw_content(self, *args, **kwargs):
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
    def draw_content(self) -> None:
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


@dataclass
class WindowStackOrientation:
    VERTICAL = 0
    HORIZONTAL = 1


class WindowStack:
    """Window stack class

    This class allow users to stack multiple window vertically or horizontally.
    """

    def __init__(self,
                 wnds: List,
                 orientation: WindowStackOrientation,
                 offset: float):
        """
        :param wnds: List of window, subclasses of ImGuiWindowAbstract.
        :param orientation: Orientation of stacked windows.
        :param offset: Fixed spaces between windows.
        """
        self._last_wnd_pos = (0.0, 0.0)
        self._last_wnd_size = (0.0, 0.0)
        self.wnds = wnds
        for wnd in self.wnds:
            wnd.before_end_functions.append(
                lambda: self.update_last_wnd_pos()
            )
            wnd.before_end_functions.append(
                lambda: self.update_last_wnd_size()
            )
        self.orientation = orientation
        self.offset = offset

    def update_last_wnd_pos(self) -> None:
        """Update _last_wnd_pos."""
        self._last_wnd_pos = imgui.get_window_position()

    def update_last_wnd_size(self) -> None:
        """Update _last_wnd_size."""
        self._last_wnd_size = imgui.get_window_size()

    def draw(self) -> None:
        for index, wnd in enumerate(self.wnds):
            wnd.draw()
            if index + 1 < len(self.wnds):
                if self.orientation == WindowStackOrientation.VERTICAL:
                    imgui.set_next_window_position(
                        self._last_wnd_pos[0],
                        self._last_wnd_pos[1] + self._last_wnd_size[1] + self.offset
                    )
                else:
                    imgui.set_next_window_position(
                        self._last_wnd_pos[0] + self._last_wnd_size[0] + self.offset,
                        self._last_wnd_pos[1]
                    )
