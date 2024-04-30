import pygame
from sq_src.data_structures.data_types import Point, Size


# class TextBox:
#     def __init__(self, center: Point, size: Size, color_active, color_inactive, font_size=32, text=''):
#         # Calculate the top-left corner based on the center position
#         self.center = center
#         self.size = size
#         self.rect = pygame.Rect(center.x - self.size.width // 2, center.y - self.size.height // 2, self.size.width, self.size.height)
#         self.color_active = color_active
#         self.color_inactive = color_inactive
#         self.color = self.color_inactive
#         self.text = text
#         self.font = pygame.font.Font(None, font_size)
#         self.active = False

#     def draw(self, screen):
#         # Render the text.
#         text_surface = self.font.render(self.text, True, self.color)
#         # Resize the box if the text is too long.
#         width = max(self.size.width, text_surface.get_width() + 10)
#         self.rect.w = width
#         # Blit the text.
#         screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 10))
#         # Draw the rect.
#         pygame.draw.rect(screen, self.color, self.rect, 2)

#     def update(self, events):
#         for event in events:
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 # If the user clicked on the input_box rect.
#                 if self.rect.collidepoint(event.pos):
#                     # Toggle the active variable.
#                     self.active = not self.active
#                 else:
#                     self.active = False
#                 # Change the current color of the input box.
#                 self.color = self.color_active if self.active else self.color_inactive
#             if event.type == pygame.KEYDOWN:
#                 if self.active:
#                     # if event.key == pygame.K_RETURN:
#                     #     print(self.text)  # You could also add a callback here
#                     #     self.text = ''  # Optionally clear the text.
#                     if event.key == pygame.K_BACKSPACE:
#                         self.text = self.text[:-1]
#                     else:
#                         self.text += event.unicode






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
                        self.text += event.unicode


