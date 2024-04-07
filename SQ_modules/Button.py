import pygame
from SQ_modules.DataTypes import Point
from SQ_modules.Sprites import TextSprite

class Button:
    def __init__(self, screen, color, center_pos: Point, width, height, font_file: str, font_size: int, text='', font_color=(0, 0, 0), outline_color=None, hover_color=None):
        """
        Initializes a new Button object.

        Parameters:
        - screen: The pygame surface on which the button will be drawn.
        - color: The primary color of the button.
        - center_pos (Point): The center position of the button on the screen.
        - width: The width of the button.
        - height: The height of the button.
        - font_file (str): The file path or name of the font to use for the button's text.
        - font_size (int): The size of the font.
        - text (str, optional): The text to display on the button. Defaults to an empty string.
        - font_color (tuple, optional): The color of the font as an RGB tuple. Defaults to black (0, 0, 0).
        - outline_color (optional): The color of the button's outline. If None, the button will not have an outline.
        - hover_color (optional): The color of the button when the mouse hovers over it. If None, it defaults to the primary color.

        This constructor initializes the button with the specified attributes and prepares the text label to be displayed on the button.
        """
        self.screen = screen
        self.color = color
        self.color_copy = color
        self.center_pos = center_pos
        self.width = width
        self.height = height
        self.text = text
        self.font_color = font_color
        self.outline_color = outline_color
        self.hover_color = hover_color if hover_color is not None else color
        self.font_file = font_file
        self.font_size = font_size

        # Calculate the top left position based on the center position
        self.top_left = Point(center_pos.x - (width // 2), center_pos.y - (height // 2))

        # Create the text sprite for the button's label
        self.label = TextSprite(text, font_file, font_size, center_pos, font_color, anchor='center')

        # Create a sprite group for easy rendering
        self.label_sprite_group = pygame.sprite.Group()
        self.label_sprite_group.add(self.label)

    def is_over(self, pos) -> bool:
        """
        Determines if the specified mouse position is over the button.

        Parameters:
        - pos: A tuple (x, y) representing the current mouse position.

        Returns:
        - True if the mouse position is over the button, False otherwise.
        """
        return self.top_left.x < pos[0] < self.top_left.x + self.width and \
               self.top_left.y < pos[1] < self.top_left.y + self.height

    def draw(self):
        """
        Draws the button on the screen. This includes the button's background color,
        optional outline, and text label.
        """
        # Draw the button's outline if specified
        if self.outline_color:
            pygame.draw.rect(self.screen, self.outline_color, (self.top_left.x - 2, self.top_left.y - 2, self.width + 4, self.height + 4))

        # Draw the button's background
        pygame.draw.rect(self.screen, self.color, (self.top_left.x, self.top_left.y, self.width, self.height))

        # Draw the button's text label
        self.label_sprite_group.draw(self.screen)

    def update(self, events: list[pygame.event.Event]):
        """
        Updates the button's appearance based on user interactions.

        Parameters:
        - events: A list of pygame events to process, typically passed from the event loop.

        This method checks for mouse movement over the button and updates the button's color
        to reflect hover state.
        """
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.color = self.hover_color if self.is_over(event.pos) else self.color_copy