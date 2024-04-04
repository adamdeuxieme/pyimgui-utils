from typing import Callable, List, Tuple

import OpenGL.GL as gl
import imgui
import pygame
from typing_extensions import override

from examples.utils import draw_square, setup_imgui_context
from pyimgui_utils import BasicWindow, DragButtons


class SquarePositionWindow(BasicWindow):
    """A Window to alter square positions.

    Contain 3 set of drag buttons, on set for each square on the screen.
    The same DragButtons instance is reuse for each square. It allows to reuse
    parameters as  drag_min, drag_max and drag_speed.
    """

    def __init__(self):
        super().__init__(
            name="Square Position"
        )
        self.drag_buttons = DragButtons(
            drag_min=-1,
            drag_max=1,
            drag_speed=0.01,
        )

    @override
    def draw_content(self,
                     pos_setters: List[Tuple[List[float], List[Callable[[float], None]]]],
                     format_table: List[str]) -> None:
        """Draw the main content of the SquarePositionWindow instance

        :param pos_setters: List of two-elements tuples. The first element is
        position values and the second element is a list of setters, one setter
        for each value in position list.
        :param format_table: A list of strings used to set the formatting of
        the drag buttons.
        """
        imgui.text("Alter squares position in this window.")
        for el in pos_setters:
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
    def setter_factory(position: List[float],
                       index: int) -> Callable[[float], None]:
        def setter(x: float):
            position[index] = x
        return setter

    # Use the setters factory to create a list of setters.
    setters_square_1 = [setter_factory(square_position_1, i) for i in range(2)]
    setters_square_2 = [setter_factory(square_position_2, i) for i in range(2)]
    setters_square_3 = [setter_factory(square_position_3, i) for i in range(2)]

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
            pos_setters=[
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
