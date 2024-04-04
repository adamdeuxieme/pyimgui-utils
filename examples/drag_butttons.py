from typing import Callable, List, Tuple

import OpenGL.GL as gl
import imgui
import pygame
from typing_extensions import override

from examples.utils import draw_square, setup_imgui_context
from pyimgui_utils import BasicWindow, DragButtons


class SquarePositionWindow(BasicWindow):

    def __init__(self):
        super().__init__(
            window_name="Square Position"
        )
        self.drag_buttons = DragButtons(
            drag_min=-1,
            drag_max=1,
            drag_speed=0.01,
        )

    @override
    def draw_content(self,
                     pos_callback: List[Tuple[List[float], List[Callable[[float], None]]]],
                     format_table: List[str]) -> None:
        imgui.text("Alter square position in this window.")
        for el in pos_callback:
            position = el[0]
            setters = el[1]
            self.drag_buttons.draw(values=position,
                                   setters=setters,
                                   format_table=format_table)
            imgui.new_line()


def main():
    impl = setup_imgui_context()

    square_position_1 = [0., 0.]
    square_position_2 = [0., 0.]
    square_position_3 = [0., 0.]

    # Create a setter factory.
    # Bind each values of position attribute with a setter.
    def set_factory(index: int, position):
        def set_position(x: float):
            position[index] = x
        return set_position

    # Use the setters factory to create a list of setters.
    setters_square_1 = [set_factory(i, square_position_1) for i in range(2)]
    setters_square_2 = [set_factory(i, square_position_2) for i in range(2)]
    setters_square_3 = [set_factory(i, square_position_3) for i in range(2)]

    # Create a format table
    format_table = ["x:%f", "y:%f"]

    # Create the SquarePositionWindow
    square_position_window = SquarePositionWindow()

    should_stop_flag = False
    while not should_stop_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_stop_flag = True
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()

        # Draw the window with position and setters as parameters
        square_position_window.draw(
            pos_callback=[
                (square_position_1, setters_square_1),
                (square_position_2, setters_square_2),
                (square_position_3, setters_square_3),
            ],
            format_table=format_table
        )

        gl.glClearColor(0.3, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        draw_square(square_position_1, (1, 0, 0))
        draw_square(square_position_2, (0, 1, 0))
        draw_square(square_position_3, (0, 0, 1))

        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()

    impl.shutdown()


if __name__ == "__main__":
    main()
