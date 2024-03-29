from pyimgui_utils import BasicWindow, NodeTree, Button
from tests.interactive_tests.utils import run_test_window
from tests.test_config import INTERACTIVE_ENABLED


class Node:

    def __init__(self, name: str):
        self.name = name
        self.children = []


class TestNodeTreeWindow(BasicWindow):

    def __init__(self):
        super().__init__(window_name="Node tree test window")
        self.node_root = Node(name="root")
        self.node_child1 = Node(name="child 1")
        self.node_child2 = Node(name="child 2")
        self.node_root.children = [self.node_child1, self.node_child2]
        self.switch_case_btn = Button(
            label="SC",
            btn_callback=self.switch_case
        )
        self.node_tree_component = NodeTree(
            btns=[self.switch_case_btn]
        )

    @staticmethod
    def switch_case(node: Node) -> None:
        """Switch upper/lower case of node name."""
        node.name = node.name.upper() \
            if node.name.islower() \
            else node.name.lower()

    def draw_content(self, *args, **kwargs) -> None:
        self.node_tree_component.draw(
            elements=[self.node_root],
            get_children=lambda node: node.children,
        )


class TestNodeTreeInteractive:

    def test_node_tree_with_button(self):
        if INTERACTIVE_ENABLED:
            wd_ut = TestNodeTreeWindow()
            run_test_window(
                window_under_test=wd_ut,
                expected_behavior=["You should see a node tree with 3 nodes.",
                                   "A button SC should switch node case on click.",
                                   "Every button should be align on the left.",
                                   "Node tree offset should be visible."]
            )
