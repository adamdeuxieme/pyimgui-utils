from __future__ import annotations
import math

import imgui
import pytest

from pyimgui_utils import Button, DragButtons, NodeTree
from tests.utils import setup_imgui_context, terminate_imgui_context


class TestButton:

    def test_init_button(self):
        msg = []
        btn = Button(label="TestButton",
                     btn_callback=lambda: msg.append("clicked!"))

        assert btn._label == "TestButton"
        btn._btn_callback()
        assert msg == ["clicked!"]

        hold_btn_color = (.5, .5, .0)
        btn_holdable = Button(label="TestButtonHoldable",
                              btn_callback=lambda: msg.append("holdable!"),
                              hold_condition=lambda: True,
                              hold_btn_color=hold_btn_color)

        assert btn_holdable._hold_condition()
        assert btn_holdable._hold_btn_color == hold_btn_color
        assert btn_holdable._hold_btn_color_hovered == hold_btn_color
        assert btn_holdable._hold_btn_color_active == hold_btn_color

        hold_btn_hovered = (.0, .5, .5)
        btn_holdable_hovered = (
            Button(label="TestButtonHoldable",
                   btn_callback=lambda: msg.append("holdable!"),
                   hold_condition=lambda: True,
                   hold_btn_color=hold_btn_color,
                   hold_btn_color_hovered=hold_btn_hovered))

        assert btn_holdable_hovered._hold_condition()
        assert btn_holdable_hovered._hold_btn_color == hold_btn_color
        assert btn_holdable_hovered._hold_btn_color_hovered == hold_btn_hovered
        assert btn_holdable_hovered._hold_btn_color_active == hold_btn_color

        hold_btn_active = (.5, .0, .5)
        btn_holdable_active = (
            Button(label="TestButtonHoldable",
                   btn_callback=lambda: msg.append("holdable!"),
                   hold_condition=lambda: True,
                   hold_btn_color=hold_btn_color,
                   hold_btn_color_hovered=hold_btn_hovered,
                   hold_btn_color_active=hold_btn_active))

        assert btn_holdable_active._hold_condition()
        assert btn_holdable_active._hold_btn_color == hold_btn_color
        assert btn_holdable_active._hold_btn_color_hovered == hold_btn_hovered
        assert btn_holdable_active._hold_btn_color_active == hold_btn_active

    def test_draw(self):
        impl, _, ctx = setup_imgui_context()

        msg = []
        hold_btn_color = (.0, .5, .5)
        hold_btn_hovered = (.5, .0, .5)
        hold_btn_active = (.5, .5, .0)

        btn_holdable_active = (
            Button(label="TestButtonHoldable",
                   btn_callback=lambda: msg.append("holdable!"),
                   hold_condition=lambda: True,
                   hold_btn_color=hold_btn_color,
                   hold_btn_color_hovered=hold_btn_hovered,
                   hold_btn_color_active=hold_btn_active))

        try:
            imgui.new_frame()
            btn_holdable_active.draw()
            imgui.render()
        finally:
            terminate_imgui_context(impl, ctx)


class TestDragButton:

    def test_init_drag_button(self):
        drag_min = .0
        drag_max = 1.
        drag_speed = .001
        btn_width = 10.
        drag_button = DragButtons(
            drag_min=drag_min,
            drag_max=drag_max,
            drag_speed=drag_speed,
            btn_width=btn_width
        )

        assert math.isclose(drag_button._drag_min,
                            drag_min,
                            rel_tol=1e-09,
                            abs_tol=1e-09)
        assert math.isclose(drag_button._drag_max,
                            drag_max,
                            rel_tol=1e-09,
                            abs_tol=1e-09)
        assert math.isclose(drag_button._drag_speed,
                            drag_speed,
                            rel_tol=1e-09,
                            abs_tol=1e-09)
        assert math.isclose(drag_button._btn_width,
                            btn_width,
                            rel_tol=1e-09,
                            abs_tol=1e-09)
        assert drag_button._title is None

        title = "Title"
        drag_button_with_title = DragButtons(
            drag_min=drag_min,
            drag_max=drag_max,
            drag_speed=drag_speed,
            btn_width=btn_width,
            title=title
        )

        assert drag_button_with_title._title == title

    def test_draw(self):
        impl, _, ctx = setup_imgui_context()
        drag_min = .0
        drag_max = 1.
        drag_speed = .001
        btn_width = 10.
        drag_button = DragButtons(
            drag_min=drag_min,
            drag_max=drag_max,
            drag_speed=drag_speed,
            btn_width=btn_width
        )

        try:
            imgui.new_frame()
            drag_button.draw(values=[1, 2, 3],
                             callbacks=[lambda e: None for _ in range(3)],
                             format_table=["x:%0.3f", "y:%0.3f", "z:%0.3f"])
            imgui.render()
        finally:
            terminate_imgui_context(impl, ctx)


class TestNodeTree:

    def test_init_node_tree(self):
        btns = [Button(label="D",
                       btn_callback=lambda: None)]
        offset = 20
        node_tree = NodeTree(
            btns=btns,
            tree_child_offset=offset
        )

        assert node_tree._btns == btns, "btns list is invalid!"
        assert node_tree._tree_child_offset == offset, "offset is invalid!"

        with pytest.raises(TypeError):
            NodeTree(
                btns=Button(label="",
                            btn_callback=lambda: None)
            )

        with pytest.raises(TypeError):
            NodeTree(
                btns="invalid value"
            )

    def test_draw(self):
        impl, _, ctx = setup_imgui_context()

        btns = [Button(label="D",
                       btn_callback=lambda: None)]
        offset = 20
        node_tree = NodeTree(
            btns=btns,
            tree_child_offset=offset
        )

        class Element:

            def __init__(self, name: str):
                self.name = name
                self.children = []

        el1 = Element("el1")
        el2 = Element("el2")
        el11 = Element("el11")
        el1.children.append(el11)
        elements = [el1, el2]

        try:
            imgui.new_frame()
            node_tree.draw(elements, lambda e: e.children)
            imgui.render()
        finally:
            terminate_imgui_context(impl, ctx)
