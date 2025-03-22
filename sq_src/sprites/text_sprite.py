import pygame

from sq_src.data_structures.data_types import Point, Anchor


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text: str, font_file: str, font_size: int, location: Point, color: tuple = (0,0,0), anchor: Anchor = Anchor.CENTER, outline_color: tuple = None, outline_width: int = 2):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(font_file, font_size)
        self.color = color
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.anchor = anchor
        self.location = location
        self.update_text(text)
        
    def render_text_with_outline(self, text: str):
        # Render the base text
        base_text = self.font.render(text, True, self.color)
        if not self.outline_color:
            return base_text
        
        # Create a surface to hold the text with an outline
        outline_surface = pygame.Surface(base_text.get_rect().inflate(self.outline_width*2, self.outline_width*2).size, pygame.SRCALPHA)
        
        # Render the outline by blitting the base text multiple times with an offset
        outline_rect = base_text.get_rect()
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # You can add more directions for a thicker outline
            outline_surface.blit(self.font.render(text, True, self.outline_color), (outline_rect.x + dx*self.outline_width, outline_rect.y + dy*self.outline_width))
        
        # Blit the base text onto the outline surface
        outline_surface.blit(base_text, (self.outline_width, self.outline_width))
        return outline_surface
        
    def update_text(self, text: str):
        self.text = text
        self.image = self.render_text_with_outline(text)
        self.rect = self.image.get_rect()
        if self.anchor == Anchor.CENTER:
            self.rect.center = self.location
        elif self.anchor == Anchor.TOP_LEFT:
            self.rect.topleft = self.location
        elif self.anchor == Anchor.TOP_RIGHT:
            self.rect.topright = self.location
        elif self.anchor == Anchor.BOTTOM_LEFT:
            self.rect.bottomleft = self.location
        elif self.anchor == Anchor.BOTTOM_RIGHT:
            self.rect.bottomright = self.location
        else:
            raise ValueError("Invalid anchor point")

    def update_text_color(self, color):
        self.color = color
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect()
        self.update_text(self.text)