




import pygame

from sq_src.configs import BLACK, DARK_GRAY, GRAY, TITLE_FONT, WINDOW_DIMENSIONS
from sq_src.controls.rectangle import Rectangle
from sq_src.data_structures.data_types import Point
from sq_src.sprites.text_sprite import TextSprite

class NotificationBanner(pygame.sprite.Sprite):
    """
    A class representing a notification banner that displays text on the screen.

    This banner is a Pygame sprite that can be added to a sprite group for rendering.
    It displays text with customizable appearance and includes a loading bar to
    indicate the remaining display time.

    Attributes:
        text (str): The text to display on the banner.
        duration (float): The duration (in seconds) that the banner is displayed.
        start_time (int): The time (in milliseconds) when the banner was created.
        bg_color (tuple): The background color of the banner (RGB tuple).
        text_color (tuple): The color of the text (RGB tuple).
        outline_color (tuple): The color of the banner's outline (RGB tuple, or None for no outline).
        outline_thickness (int): The thickness of the outline (in pixels).
        font_file (str): The path to the font file.
        font_size (int): The size of the font.
        border_radius (int): The radius of the banner's rounded corners.
        width (int): The width of the banner.
        height (int): The height of the banner.
        loading_bar_color (tuple): The color of the loading bar (RGB tuple).
        loading_bar_width (int): The current width of the loading bar.
        image (pygame.Surface): The Pygame surface representing the banner.
        rect (pygame.Rect): The rectangle representing the banner's position and size.
        font (pygame.font.Font): The Pygame font object.
    """

    def __init__(self, text, duration=10,
                 bg_color=GRAY,
                 text_color=BLACK,
                 outline_color=None,
                 outline_thickness=2,
                 font_file=TITLE_FONT,
                 font_size=36,
                 border_radius=4,
                 width=200,
                 height=70,
                 loading_bar_color=DARK_GRAY):
        """
        Initializes the NotificationBanner.

        Args:
            text (str): The text to display.
            duration (float): The display duration in seconds.
            bg_color (tuple): The background color (default: GRAY).
            text_color (tuple): The text color (default: BLACK).
            outline_color (tuple): The outline color (default: None).
            outline_thickness (int): The outline thickness (default: 2).
            font_file (str): The font file path (default: TITLE_FONT).
            font_size (int): The font size (default: 36).
            border_radius (int): The border radius (default: 4).
            width (int): The banner width (default: 200).
            height (int): The banner height (default: 70).
            loading_bar_color (tuple): The loading bar color (default: DARK_GRAY).
        """
        super().__init__()
        self.text = text
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.bg_color = bg_color
        self.text_color = text_color
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.font_file = font_file
        self.font_size = font_size
        self.border_radius = border_radius
        self.width = width
        self.height = height
        self.loading_bar_color = loading_bar_color
        self.loading_bar_width = 0

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        if outline_color:
            pygame.draw.rect(self.image, outline_color, self.image.get_rect(), border_radius=border_radius)
            inner_rect = pygame.Rect(outline_thickness, outline_thickness, width - 2 * outline_thickness, height - 2 * outline_thickness)
            pygame.draw.rect(self.image, bg_color, inner_rect, border_radius=max(0, border_radius - outline_thickness))
        else:
            pygame.draw.rect(self.image, bg_color, self.image.get_rect(), border_radius=border_radius)

        self.font = pygame.font.Font(font_file, font_size)
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)

        # Positioning the banner in the bottom right
        self.rect = self.image.get_rect(bottomright=(WINDOW_DIMENSIONS.width - 10, WINDOW_DIMENSIONS.height - 10))

    def update(self):
        """
        Updates the banner's state, including its duration and loading bar.
        Removes the banner if its duration has elapsed.
        """
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        if elapsed_time > self.duration:
            self.kill()
            return

        self.loading_bar_width = int((elapsed_time / self.duration) * self.width)
        self.draw_loading_bar()

    def draw_loading_bar(self):
        """
        Draws the loading bar on the banner's image.
        """
        loading_bar_rect = pygame.Rect(0, 0, self.loading_bar_width, 5)
        pygame.draw.rect(self.image, self.loading_bar_color, loading_bar_rect)