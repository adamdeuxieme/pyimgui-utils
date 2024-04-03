from abc import ABC, abstractmethod


class DrawableIT(ABC):
    """Object that can be drawn on the screen in an imgui context.

    It has at least one method draw that takes any parameters and
    draw content on the screen.
    """

    @abstractmethod
    def draw(self, *args, **kwargs) -> None:
        """Draw the content in an imgui context."""
        pass
