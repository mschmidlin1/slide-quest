




import pygame

from sq_src.data_structures.data_types import Point


class Rectangle:
    """
    A class representing a simple rectangle shape in Pygame.

    This class provides functionality to draw a rectangle with optional outline and rounded corners.
    It serves as a base class for other interactive elements like buttons.

    Attributes:
        screen (pygame.Surface): The Pygame surface on which the rectangle will be drawn.
        color (tuple): The RGB color of the rectangle's fill.
        color_copy (tuple): A copy of the original color, used for reverting after hover effects (if applicable).
        center_pos (Point): A Point object representing the center position of the rectangle.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        outline_color (tuple, optional): The RGB color of the rectangle's outline. Defaults to None (no outline).
        border_radius (int, optional): The radius of the rectangle's rounded corners. Defaults to 10.
        top_left (Point): A Point object representing the top-left position of the rectangle.
    """

    def __init__(self, screen, color, center_pos: 'Point', width, height, outline_color=None, border_radius=10):
        """
        Initializes a new Rectangle object.

        Args:
            screen (pygame.Surface): The Pygame surface on which the rectangle will be drawn.
            color (tuple): The RGB color of the rectangle's fill.
            center_pos (Point): A Point object representing the center position of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            outline_color (tuple, optional): The RGB color of the rectangle's outline. Defaults to None (no outline).
            border_radius (int, optional): The radius of the rectangle's rounded corners. Defaults to 10.
        """
        self.screen = screen
        self.color = color
        self.color_copy = color
        self.center_pos = center_pos
        self.width = width
        self.height = height
        self.outline_color = outline_color
        self.border_radius = border_radius

        self.top_left = Point(center_pos.x - (width // 2), center_pos.y - (height // 2))

    def draw(self):
        """
        Draws the rectangle on the screen.

        This method draws the rectangle with its fill color, optional outline, and rounded corners.
        """
        if self.outline_color:
            pygame.draw.rect(self.screen, self.outline_color,
                             (self.top_left.x - 2, self.top_left.y - 2, self.width + 4, self.height + 4),
                             border_radius=self.border_radius + 2)

        pygame.draw.rect(self.screen, self.color,
                         (self.top_left.x, self.top_left.y, self.width, self.height),
                         border_radius=self.border_radius)

    def update(self, events: list['pygame.event.Event']):
        """
        Updates the rectangle's state based on events.

        This method is intended to be overridden by subclasses to add specific update logic.
        In the base Rectangle class, it does nothing.

        Args:
            events (list[pygame.event.Event]): A list of Pygame events to process.
        """
        pass