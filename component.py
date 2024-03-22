import logging
from typing import Union, Callable, Tuple, Optional

import imgui


class DragButtons:

    def __init__(self,
                 drag_min: Union[float, int],
                 drag_max: Union[float, int],
                 drag_speed: Union[float, int] = 1.0,
                 btn_width: Union[int, float] = 220,
                 title: Union[str, None] = None):  # todo: switch to Optional in hint
        """DragButton row.

        Facilitate build of drag buttons row creation.
        :param drag_min:   drag buttons min value
        :param drag_max:   drag buttons max value.
        :param drag_speed: drag buttons speed
        :param btn_width:  drag buttons width
        :param title:      Optional drag button title
        """
        self._btn_width = btn_width
        self._drag_min = drag_min
        self._drag_max = drag_max
        self._drag_speed = drag_speed
        self._title = None if title is not None and title == "" else title

        if self._title is not None:  # todo: Remove it, shouldn't be in main
            print(f"title: {self._title} id:{id(self)}")

    def draw(self,
             values: Union[list[float], list[int]],
             callbacks: list[Callable[[Union[float, int]], None]],
             format_table: Union[list[str], None] = None):  # todo: switch to Optional in hint

        btn_nb = len(callbacks)

        for i in range(btn_nb):
            btn_id = f"{id(self)}{i}"  # Must be unique to ensure correct callback binding
            imgui.set_next_item_width(self._btn_width)

            if format_table is not None:
                imgui.push_id(btn_id)  # todo: move the previous scope
                changed, value = imgui.drag_float("",
                                                  values[i],
                                                  self._drag_speed,
                                                  self._drag_min,
                                                  self._drag_max,
                                                  format_table[i])
                imgui.pop_id()

            else:
                imgui.push_id(btn_id)  # todo: move the previous scope
                changed, value = imgui.drag_float("",
                                                  values[i],
                                                  self._drag_speed,
                                                  self._drag_min,
                                                  self._drag_max)
                imgui.pop_id()

            if changed:
                callbacks[i](value)

            if i + 1 >= btn_nb and self._title is not None:
                imgui.same_line()
                imgui.text(self._title)

            else:
                imgui.same_line()


class Button:

    def __init__(self,  # todo: Use Optional hint for attributes down here
                 label: str,
                 btn_callback: Callable[..., None],
                 hold_condition: Optional[Callable[..., bool]] = None,
                 hold_btn_color: Optional[Tuple[float, float, float]] = None,
                 hold_btn_color_hovered: Optional[Tuple[float, float, float]] = None,
                 hold_btn_color_active: Optional[Tuple[float, float, float]] = None,
                 width: int = 0,
                 height: int = 0):
        """Advance imgui button
        It embeds more features than classic imgui button. For instance, it is possible to hold the button color.

        :param label:                  Displayed name of the button
        :param btn_callback:           Callback function when button is pressed
        :param hold_condition:         Callable function that return true if the button needs to be held,
                                       false otherwise
        :param hold_btn_color:         A tuple corresponding to the rgb color tuple when button is held
        :param hold_btn_color_hovered: a tuple corresponding to the rgb color tuple when button is held and hovered
        :param hold_btn_color_active:  a tuple corresponding to the rgb color tuple when button is held and active
        :param width:                  Width of the button
        :param height:                 Height of the button
        """

        self._label = label
        self._btn_callback = btn_callback
        self._hold_condition = hold_condition

        # todo: change default color
        self._hold_btn_color = [0.973, 0.514, 0.027] if hold_btn_color is None else hold_btn_color

        if hold_btn_color_hovered is None:
            self._hold_btn_color_hovered = self._hold_btn_color
        else:
            self._hold_btn_color_hovered = hold_btn_color_hovered

        if hold_btn_color_active is None:
            self._hold_btn_color_active = self._hold_btn_color
        else:
            self._hold_btn_color_active = hold_btn_color_active

        self._width = width
        self._height = height

    def draw(self, *args, **kwargs) -> None:
        """Draw button."""

        hold_flag = self._hold_condition(*args, **kwargs) if self._hold_condition is not None else False

        if hold_flag:
            imgui.push_style_color(imgui.COLOR_BUTTON, *self._hold_btn_color, 1.0)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *self._hold_btn_color_hovered, 1.0)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *self._hold_btn_color_active, 1.0)

        if imgui.button(self._label, self._width, self._height):
            self._btn_callback(*args, **kwargs)

        if hold_flag:
            imgui.pop_style_color(3)  # both neutral, hovered and active button color styles.


class NodeTree:

    def __init__(self,
                 btns: list[Union[Button]] = None,
                 tree_child_offset: int = 10):
        """Node tree
        Draw a node tree with optional buttons on the left side.

        :param btns: List of Buttons (from this module)
        :param tree_child_offset: Custom offset of the tree (default 10)
        """
        if btns is not None:
            if (not isinstance(btns, list)
                    or not all(isinstance(el, Button)
                               or isinstance(el, Button) for el in btns)):
                raise TypeError("btns must be a list of HoldableButton or Buttons!")
            else:
                self._btns = btns
        else:
            self._btns = None

        self._tree_child_offset = tree_child_offset

    def draw(self, elements: list, get_children: Callable) -> None:
        """Draw the node tree with elements list.

        :param elements: list of elements represented a node tree
        :param get_children: function to access elements' children.
        """

        self._display_node_tree(elements=elements,
                                get_children=get_children,
                                btn_cur_pos=imgui.get_cursor_pos_x())

    def _display_node_tree(self,
                           elements: list,
                           get_children: Callable,
                           btn_cur_pos: float,
                           offset: float = 0) -> None:
        """This is a recursive method that display the tree node.

        :param elements: list of elements to display
        :param get_children: Function to call on elements to get their children
        :param btn_cur_pos: The button position.
        :param offset: Offset of tree levels.
        """

        if not isinstance(elements, list):
            raise TypeError("elements must be a list!")

        if not isinstance(btn_cur_pos, float):
            raise TypeError("btn_cur_pos must be a float!")

        if not (isinstance(offset, float) or isinstance(offset, int)):
            raise TypeError("offset must be either a float or an int!")

        if offset < 0:
            raise ValueError("offset must be positive!")

        for el in elements:

            imgui.set_cursor_pos_x(btn_cur_pos)  # Draw each button at the same position

            if self._btns is not None:
                for btn in self._btns:
                    imgui.push_id(f"{id(el)}{id(btn)}")
                    btn.draw(el)
                    imgui.pop_id()
                    imgui.same_line()

            tree_input_cursor_position = imgui.get_cursor_pos_x() + offset
            imgui.set_cursor_pos_x(tree_input_cursor_position)  # Put the cursor back it tree level position

            if imgui.tree_node(el.name):
                display_tree_offset = self._tree_child_offset
                self._display_node_tree(get_children(el), get_children, btn_cur_pos, offset + display_tree_offset)
                imgui.tree_pop()
