import imgui

import pytest
from typing_extensions import override

from pyimgui_utils import ImGuiWindowAbstract
from tests.utils import setup_imgui_context


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
        setup_imgui_context()

        class ClassUnderTest(Window):
            def __init__(self):
                super().__init__()
                self.call_order = []
                self._before_begin_functions.append(
                    lambda: self.call_order.append(1)
                )
                self._after_begin_functions.append(
                    lambda: self.call_order.append(2)
                )
                self._before_end_functions.append(
                    lambda: self.call_order.append(3)
                )
                self._after_end_functions.append(
                    lambda: self.call_order.append(4)
                )

        cls_ut = ClassUnderTest()
        imgui.new_frame()
        cls_ut.draw()
        imgui.render()

        assert cls_ut.call_order == [1, 2, 3, 4], "Function call order not respected"
