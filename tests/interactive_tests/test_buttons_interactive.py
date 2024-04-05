from typing import Callable, List

import imgui
from typing_extensions import override

from pyimgui_utils import BasicWindow, Button, DragButtons
from tests.interactive_tests.utils import run_test_window
from tests.test_config import INTERACTIVE_ENABLED


class TestButtonWindow(BasicWindow):

    def __init__(self):
        super().__init__(name="Test button window")
        self.counter = 0
        self.btn = Button(label="Increase",
                          btn_callback=self.increase_count)

    def increase_count(self):
        self.counter += 1

    @override
    def draw_content(self) -> None:
        self.btn.draw()
        imgui.text(f"self.counter = {self.counter}")


class TestButtonSameNameWindow(BasicWindow):

    def __init__(self):
        super().__init__(
            name="Test button same name window"
        )
        self.counter_1 = 0
        self.counter_2 = 0

        self.btn_1 = Button(
            label="Increment",
            btn_callback=lambda: self.increase_counter_1()
        )

        self.btn_2 = Button(
            label="Increment",
            btn_callback=lambda: self.increase_counter_2()
        )

    def increase_counter_1(self):
        self.counter_1 += 1

    def increase_counter_2(self):
        self.counter_2 += 1

    @override
    def draw_content(self, *args, **kwargs) -> None:
        imgui.text(f"self.counter_1 = {self.counter_1}")
        imgui.text(f"self.counter_2 = {self.counter_2}")
        self.btn_1.draw()
        imgui.same_line()
        self.btn_2.draw()


class TestDragButtonWindow(BasicWindow):

    def __init__(self):
        super().__init__(name="Test drag button window")
        self.values = [0, 0, 0, 0, 0]
        self.format_table = ["x:%0.1f",
                             "y:%0.1f",
                             "z:%0.1f",
                             "a:%0.1f",
                             "b:%0.1f"]
        self.setters = [self.set_value_factory(i) for i in range(5)]
        self.drag_btns = DragButtons(
            drag_min=-5.,
            drag_max=5.,
            drag_speed=0.05,
            btn_width=50.,
            title="title"
        )

    def set_value_factory(self, index: int):
        def set_value(value):
            self.values[index] = value

        return set_value

    @override
    def draw_content(self, *args, **kwargs) -> None:
        self.drag_btns.draw(
            values=self.values,
            setters=self.setters,
            format_table=self.format_table
        )


class TestDragButtonSameName(BasicWindow):
    """Ensure drag buttons are reusable within the same window."""

    def __init__(self):
        super().__init__(
            name="TestDragButtonSameName"
        )

        self.drag_btns = DragButtons(
            drag_min=-10.0,
            drag_max=10.0,
            drag_speed=0.1
        )

        self.position = [0.0, 0.0]
        self.acceleration = [0.0, 0.0]
        self.setters_pos = [self.setters_factory(self.position, i)
                            for i in range(2)]
        self.setters_ac = [self.setters_factory(self.acceleration, i)
                           for i in range(2)]

    def draw_content(self, *args, **kwargs) -> None:
        imgui.text(f"self.position = {self.position}")
        self.drag_btns.draw(self.position, self.setters_pos)
        imgui.new_line()
        imgui.text(f"self.acceleration = {self.acceleration}")
        self.drag_btns.draw(self.acceleration, self.setters_ac)

    @staticmethod
    def setters_factory(values: List[float],
                        index: int) -> Callable[[float], None]:
        def setter(value: float) -> None:
            values[index] = value

        return setter


class TestButtonsInteractive:

    def test_button(self):
        if INTERACTIVE_ENABLED:
            wd_ut = TestButtonWindow()
            run_test_window(
                window_under_test=wd_ut,
                expected_behavior=["You should see a button. On press ",
                                   "the number of clicked count "
                                   "should increases."]
            )

    def test_button_same_name(self):
        if INTERACTIVE_ENABLED:
            wd_ut = TestButtonSameNameWindow()
            run_test_window(
                window_under_test=wd_ut,
                expected_behavior=["Two buttons are in the same window with "
                                   "the same name.",
                                   "Button on the left should increase "
                                   "counter 1",
                                   "Button on the right should increase "
                                   "counter 2"]
            )

    def test_drag_buttons(self):
        if INTERACTIVE_ENABLED:
            wd_ut = TestDragButtonWindow()
            run_test_window(
                window_under_test=wd_ut,
                expected_behavior=["You should see drag buttons. On dragging "
                                   "the corresponding value should change. ",
                                   "format table must be like this 'x:0.0'. "
                                   "Min value must be -5.0 and max value must ",
                                   "be 5.0. Drag speed must be 0.05 and width "
                                   "50.0"]
            )

    def test_drag_buttons_with_same_name(self):
        if INTERACTIVE_ENABLED:
            wd_ut = TestDragButtonSameName()
            run_test_window(
                window_under_test=wd_ut,
                expected_behavior=["Observe a window with position and "
                                   "acceleration values and two set of two ",
                                   "drag buttons. You should be able to change "
                                   "position and acceleration values with the ",
                                   "drag buttons. This test demonstrate the "
                                   "ability to reuse a DragButton instance ",
                                   "for multiple values and setters within the "
                                   "same window. "]
            )
