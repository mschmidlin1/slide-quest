import pygame
from SQ_modules.DataTypes import Point, Size


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
    def __init__(self, center: Point, size: Size, color_active, color_inactive, font_size=32, text=''):
        # Initialize base properties
        self.center = center
        self.size = size
        self.rect = pygame.Rect(center.x - size.width // 2, center.y - size.height // 2, size.width, size.height)
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color = self.color_active
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.active = True

    def draw(self, screen):
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


