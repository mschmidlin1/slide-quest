import pygame
from sq_src.data_structures.data_types import Point, Size



class TextBox:
    """
    This class represents a text box element for user input within a Pygame application.
    """
    def __init__(self, center: Point, size: Size, color_active, color_inactive, font_size=32, text='', active_by_default=True):
        """
        Initializes a new TextBox object.

        Args:
            center (Point): The center point of the text box.
            size (Size): The size of the text box (width and height).
            color_active (tuple): The color of the text box border when active (RGB values).
            color_inactive (tuple): The color of the text box border when inactive (RGB values).
            font_size (int, optional): The size of the font used to render the text (default: 32).
            text (str, optional): The initial text displayed within the text box (default: '').
            active_by_default (bool, optional): A flag indicating whether the text box is initially active (default: True).
        """
        self.center = center
        self.size = size
        self.rect = pygame.Rect(center.x - size.width // 2, center.y - size.height // 2, size.width, size.height)
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color = self.color_active if active_by_default else self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.active = active_by_default

    def disable(self):
        """
        Deactivates the text box, preventing user input and changing the border color to inactive.
        """
        self.active = False
        self.color = self.color_inactive

    def enable(self):
        """
        Activates the text box, allowing user input and changing the border color to active.
        """
        self.active = True
        self.color = self.color_active

    def draw(self, screen):
        """
        Draws the text box onto the provided Pygame surface.

        Args:
            screen (pygame.Surface): The Pygame surface to draw the text box on.
        """
        # Render the text
        text_surface = self.font.render(self.text, True, self.color)
        # Calculate new width and adjust if necessary
        new_width = max(self.size.width, text_surface.get_width() + 10)
        # Adjust rect width and re-center the textbox
        self.rect.width = new_width
        self.rect.x = self.center.x - self.rect.width // 2
        # Blit the text
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 10))
        # Draw the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self, events):
        """
        Processes user input events (mouse clicks and key presses) to handle text box interaction.

        Args:
            events (list[pygame.event.Event]): A list of Pygame events to process.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += self._typed_character(event)

    def _typed_character(self, event) -> str:
        """
        Character produced by a key press.

        The browser build leaves KEYDOWN.unicode empty, so fall back to the key code.
        Desktop pygame already fills unicode, and that value is used as-is.
        """
        if event.unicode:
            return event.unicode

        key = event.key
        if key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_TAB, pygame.K_BACKSPACE):
            return ""

        mods = pygame.key.get_mods()
        if pygame.K_a <= key <= pygame.K_z:
            char = chr(key)
            if mods & (pygame.KMOD_SHIFT | pygame.KMOD_CAPS):
                return char.upper()
            return char
        if pygame.K_0 <= key <= pygame.K_9:
            if mods & pygame.KMOD_SHIFT:
                return ")!@#$%^&*("[key - pygame.K_0]
            return chr(key)

        symbols = {
            pygame.K_SPACE: (" ", " "),
            pygame.K_MINUS: ("-", "_"),
            pygame.K_EQUALS: ("=", "+"),
            pygame.K_PERIOD: (".", ">"),
            pygame.K_COMMA: (",", "<"),
            pygame.K_SLASH: ("/", "?"),
            pygame.K_SEMICOLON: (";", ":"),
            pygame.K_QUOTE: ("'", '"'),
            pygame.K_LEFTBRACKET: ("[", "{"),
            pygame.K_RIGHTBRACKET: ("]", "}"),
            pygame.K_BACKSLASH: ("\\", "|"),
            pygame.K_BACKQUOTE: ("`", "~"),
        }
        pair = symbols.get(key)
        if pair is None:
            return ""
        return pair[1] if mods & pygame.KMOD_SHIFT else pair[0]


