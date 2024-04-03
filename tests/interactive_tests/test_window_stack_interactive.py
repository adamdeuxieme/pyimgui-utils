from pyimgui_utils.window import WindowStackOrientation, WindowStack
from tests.interactive_tests.utils import run_test_window
from tests.test_config import INTERACTIVE_ENABLED
from tests.utils import DummyWindow


class TestWindowStackInteractive:

    def test_window_stack_vertical(self):
        if INTERACTIVE_ENABLED:
            wnds = [DummyWindow() for _ in range(3)]
            offset = 8
            orientation = WindowStackOrientation.VERTICAL
            wd_ut = WindowStack(
                wnds=wnds,
                offset=offset,
                orientation=orientation
            )
            run_test_window(
                window_under_test=wd_ut,
                expected_behavior=["You should see a column of 3 windows, "
                                   "aligned ",
                                   "on the the left segment and stacked from "
                                   "top to bottom.",
                                   "You must observer a slight padding between "
                                   "windows",
                                   "Moving the first window on the top move "
                                   "every stacked windows."]
            )

    def test_window_stack_horizontal(self):
        if INTERACTIVE_ENABLED:
            wnds = [DummyWindow() for _ in range(3)]
            offset = 8
            orientation = WindowStackOrientation.HORIZONTAL
            wd_ut = WindowStack(
                wnds=wnds,
                offset=offset,
                orientation=orientation
            )
            run_test_window(
                window_under_test=wd_ut,
                expected_behavior=["You should see a column of 3 windows, "
                                   "aligned ",
                                   "on the the top segment and stacked from "
                                   "left to right.",
                                   "You must observer a slight padding between "
                                   "windows",
                                   "Moving the first window on the left move "
                                   "every stacked windows."]
            )
