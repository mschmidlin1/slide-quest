
import pygame

from sq_src.configs import CELL_DIMENSIONS, PALLET_HIGHLIGHT_COLOR, SELECTOR_TOOL_IMAGE, Border_Size_Lookup
from sq_src.data_structures.converters import CellToPoint
from sq_src.data_structures.data_types import Cell, Point
from sq_src.data_structures.game_enums import GameDifficulty

class Highlighter(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = "Highlighter"
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS, pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 128))
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class SelectorTool(pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__()
        self.image = SELECTOR_TOOL_IMAGE
        self.rect = self.image.get_rect()



class HollowSquareSprite(pygame.sprite.Sprite):
    def __init__(self, location: Point, thickness: int, color=PALLET_HIGHLIGHT_COLOR, transparent_color=(0, 0, 0, 0)):
        super().__init__()
        
        # Create a transparent surface with the given size
        self.image = pygame.Surface((CELL_DIMENSIONS[0]+thickness, CELL_DIMENSIONS[1]+thickness), pygame.SRCALPHA)
        
        # Draw the outer square
        pygame.draw.rect(self.image, color, self.image.get_rect(), thickness)
        
        # Draw the inner transparent square
        inner_rect = pygame.Rect(thickness, thickness, CELL_DIMENSIONS[0]//2, CELL_DIMENSIONS[1]//2)
        pygame.draw.rect(self.image, transparent_color, inner_rect)
        
        self.rect = self.image.get_rect()

        self.rect.center = location