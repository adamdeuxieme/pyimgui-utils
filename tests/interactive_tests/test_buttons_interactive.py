import imgui
from typing_extensions import override

from pyimgui_utils import BasicWindow, Button, DragButtons
from tests.interactive_tests.utils import run_test_window
from tests.test_config import INTERACTIVE_ENABLED


class TestButtonWindow(BasicWindow):

    def __init__(self):
        super().__init__(window_name="Test button window")
        self.counter = 0
        self.btn = Button(label="Increase",
                          btn_callback=self.increase_count)

    def increase_count(self):
        self.counter += 1

    @override
    def draw_content(self) -> None:
        self.btn.draw()
        imgui.text(f"{self.counter = }")


class TestButtonSameNameWindow(BasicWindow):

    def __init__(self):
        super().__init__(
            window_name="Test button same name window"
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
        imgui.text(f"{self.counter_1 = }")
        imgui.text(f"{self.counter_2 = }")
        self.btn_1.draw()
        imgui.same_line()
        self.btn_2.draw()


class TestDragButtonWindow(BasicWindow):

    def __init__(self):
        super().__init__(window_name="Test drag button window")
        self.values = [0, 0, 0, 0, 0]
        self.format_table = ["x:%0.1f",
                             "y:%0.1f",
                             "z:%0.1f",
                             "a:%0.1f",
                             "b:%0.1f"]
        self.callbacks = [self.set_value_factory(i) for i in range(5)]
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
            callbacks=self.callbacks,
            format_table=self.format_table
        )


class TestButtonsInteractive:

    def test_button(self):
        if INTERACTIVE_ENABLED:
            wd_ut = TestButtonWindow()
            run_test_window(
                window_under_test=wd_ut,
                expected_behavior=["You should see a button. On press ",
                                   "the number of clicked count should increases."]
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
                expected_behavior=["You should see drag buttons. On dragging the ",
                                   "corresponding value should change. format table ",
                                   "must be like this 'x:0.0'. Min value must be ",
                                   "-5.0 and max value must be 5.0. Drag speed must ",
                                   "be 0.05 and width 50.0"]
            )