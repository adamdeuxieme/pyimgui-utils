import imgui

import pytest
from typing_extensions import override

from pyimgui_utils import ImGuiWindowAbstract
from pyimgui_utils.window import WindowStack, WindowStackOrientation
from tests.utils import (setup_imgui_context, FixedSizeWindow,
                         terminate_imgui_context)


class Window(ImGuiWindowAbstract):

    @override
    def _begin_statement_window(self):
        return imgui.begin("Test window")

    @override
    def draw_content(self, *args, **kwargs):
        imgui.text("Hello World!")

    def __init__(self):
        super().__init__()


class TestImGuiWindowAbstract():

    def test_abstract_class_impl(self):
        """
        ImGuiWindow should be an abstract class which implies
        no instantiation.
        """
        with pytest.raises(TypeError):
            ImGuiWindowAbstract()

    def test_before_after_begin_end_methods(self):
        impl, _, ctx = setup_imgui_context()

        class ClassUnderTest(Window):
            def __init__(self):
                super().__init__()
                self.call_order = []
                self.before_begin_functions.append(
                    lambda: self.call_order.append(1)
                )
                self.after_begin_functions.append(
                    lambda: self.call_order.append(2)
                )
                self.before_end_functions.append(
                    lambda: self.call_order.append(3)
                )
                self.after_end_functions.append(
                    lambda: self.call_order.append(4)
                )

        cls_ut = ClassUnderTest()
        imgui.new_frame()
        cls_ut.draw()
        imgui.render()
        terminate_imgui_context(impl, ctx)

        assert cls_ut.call_order == [1, 2, 3, 4], \
            "Function call order not respected"


class TestWindowStack:
    small_wnd_size = (40, 50)
    small_wnd_nb = 3
    big_wnd_size = (60, 80)
    big_wnd_nb = 1
    offset = 12

    def test_window_stack_size(self):
        impl, _, ctx = setup_imgui_context()

        fixed_size_wnds = [FixedSizeWindow(*self.small_wnd_size)
                           for _ in range(self.small_wnd_nb)]
        fixed_size_wnds.append(FixedSizeWindow(*self.big_wnd_size))

        horizontal_stack = WindowStack(
            wnds=fixed_size_wnds,
            orientation=WindowStackOrientation.HORIZONTAL,
            offset=self.offset
        )

        vertical_stack = WindowStack(
            wnds=fixed_size_wnds,
            orientation=WindowStackOrientation.VERTICAL,
            offset=self.offset
        )

        imgui.new_frame()
        horizontal_stack.draw()
        vertical_stack.draw()
        imgui.render()
        terminate_imgui_context(impl, ctx)

        expected_offset_sum = 12 * 3
        expected_wnd_width_sum = (self.small_wnd_size[0] * self.small_wnd_nb
                                  + self.big_wnd_size[0])
        expected_width = expected_wnd_width_sum + expected_offset_sum
        expected_height = self.big_wnd_size[1]
        expected_size = (expected_width, expected_height)
        assert horizontal_stack.size == expected_size, \
            "Expected horizontal stack size do not match with actual one."

        expected_wnd_height_sum = (self.small_wnd_size[1] * self.small_wnd_nb
                                   + self.big_wnd_size[1])
        expected_height = expected_wnd_height_sum + expected_offset_sum
        expected_width = self.big_wnd_size[0]
        expected_size = (expected_width, expected_height)
        assert vertical_stack.size == expected_size, \
            "Expected vertical stack size do not match with actual one."
