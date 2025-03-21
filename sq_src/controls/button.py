import pygame
from sq_src.controls.rectangle import Rectangle
from sq_src.data_structures.data_types import Point, Size, Anchor
from sq_src.configs import  BLUE_ICE, GRAY_BLUE, NAVY_BLUE, UGLY_PINK, MUTE_GREEN, LIGHT_BLUE, TITLE_FONT, DARK_GRAY
from sq_src.sprites.text_sprite import TextSprite

class Button(Rectangle):
    def __init__(self, screen, color, center_pos: Point, width, height, font_file: str, font_size: int, text='', font_color=(0, 0, 0), outline_color=None, hover_color=None, hover_font_color=None, border_radius=10):
        """
        Initializes a new Button object with an optional hover effect for the text color.

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
        - hover_font_color (optional): The color of the font when the mouse hovers over the button. If None, the font color does not change on hover.
        - border_radius (int, optional): The radius of the button's rounded corners. Defaults to 10.

        This constructor initializes the button with the specified attributes and prepares the text label to be displayed on the button.
        """
        super().__init__(screen, color, center_pos, width, height, outline_color, border_radius)
        self.text = text
        self.font_color = font_color
        self.hover_font_color = hover_font_color if hover_font_color is not None else font_color
        self.font_color_copy = font_color
        self.hover_color = hover_color if hover_color is not None else color
        self.font_file = font_file
        self.font_size = font_size

        self.label = TextSprite(text, font_file, font_size, center_pos, self.font_color, anchor=Anchor.CENTER)
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
        Draws the button on the screen, including the button's background color, optional outline, and text label.
        If hover effect is enabled, changes the background and font color when the mouse is over the button.
        """
        super().draw()
        self.label_sprite_group.draw(self.screen)

    def update(self, events: list[pygame.event.Event]):
        """
        Updates the button's appearance based on user interactions.

        Parameters:
        - events: A list of pygame events to process, typically passed from the event loop.

        This method checks for mouse movement over the button and updates the button's color and text color to reflect hover state.
        """
        super().update(events)
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.is_over(event.pos):
                    self.color = self.hover_color
                    self.label.update_text_color(self.hover_font_color)
                else:
                    self.color = self.color_copy
                    self.label.update_text_color(self.font_color_copy)





class SqButton(Button):
    """
    Initializes a new SqButton object with a predefined color scheme that inverts on hover.
    
    Inherits from the Button class and sets default colors that switch between a light background with dark text,
    to a dark background with light text upon hovering.
    """
    def __init__(self, screen, center_pos: Point, width, height, font_size: int, text='', font_file=None, border_radius=None):
        """
        Initializes a new SqButton object with a predefined color scheme and hover effect.

        Inherits from the Button class and sets default colors based on a winter-themed color palette.

        Parameters:
        - screen: The pygame surface on which the button will be drawn.
        - center_pos (Point): The center position of the button on the screen.
        - width: The width of the button.
        - height: The height of the button.
        - font_size (int): The size of the font.
        - text (str, optional): The text to display on the button. Defaults to an empty string.
        """
        # Default color scheme based on the provided winter-themed image
        primary_color = LIGHT_BLUE  # Light Blue for the button background
        text_color = NAVY_BLUE      # Dark Blue for the text
        outline_color = DARK_GRAY   # Dark Gray for the button outline
        hover_color = NAVY_BLUE     # Dark Blue for the button background on hover
        hover_font_color = LIGHT_BLUE  # Light Blue for the text on hover
        if font_file==None:
            font_file = TITLE_FONT      # The font file for the text
        if border_radius==None:
            border_radius=10
        # Initialize the superclass with the default color scheme and hover effect
        super().__init__(
            screen=screen,
            color=primary_color,
            center_pos=center_pos,
            width=width,
            height=height,
            font_file=font_file,
            font_size=font_size,
            text=text,
            font_color=text_color,
            outline_color=outline_color,
            hover_color=hover_color,
            hover_font_color=hover_font_color,  # New parameter for hover text color
            border_radius=border_radius
        )