





from pygame import Surface
import pygame
from sq_src.data_structures.converters import CellToPoint


class GameSprite(pygame.sprite.Sprite):
    """A GameSprite is a sprite that is used on the gameboard which needs to toggle with the level editor."""
    def __init__(self):
        super().__init__()
    def toggle_level_editor(self):
        temp: Surface = self.image
        self.image = self.editor_image
        self.editor_image = temp
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(self.gameboard_loc, self.difficulty)