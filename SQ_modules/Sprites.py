import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SQ_modules.GameEnums import CellType, GameDifficulty
from SQ_modules.configs import CELL_DIMENSIONS, WALL_COLOR, GOAL_COLOR, ICE_COLOR, PLAYER_COLOR, PLAYER_SPEED, PALLET_HIGHLIGHT_COLOR, SELECTOR_TOOL_IMAGE, Border_Size_Lookup
from SQ_modules.DataTypes import Point, Size, Cell
from SQ_modules.my_logging import set_logger, log
from SQ_modules.Converters import PointToCell, CellToPoint
import logging


class Player(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.PLAYER
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self._layer = 2
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)
        self.current_pos = self.rect.center
        self.speed = PLAYER_SPEED
        self.moving = False

    def move(self, location: Cell):
        """
        Set's the target position for the player as long as the player is not already moving.
        """
        self.current_pos = PointToCell(self.rect.center, self.difficulty)

        #target and current position in Cell gameboard coordinates, but needs to be in x,y order        
        self.current_pos = pygame.Vector2((self.current_pos.col, self.current_pos.row))
        self.target_pos = pygame.Vector2(location.col, location.row)

        logging.info(f"Starting Position:  {self.current_pos}  Target Position:  {self.target_pos}")

        self.moving = True

    def update(self):
        if self.moving:
            
            self.target_pos_pixels = CellToPoint(self.target_pos, self.difficulty)

            if self.rect.center == self.target_pos_pixels:
                self.moving = False
                return
            
            distance_to_target = self.target_pos - self.current_pos
            distance_to_target_length = distance_to_target.length()
            
            if distance_to_target_length < self.speed:
                self.rect.center = self.target_pos_pixels
                self.moving = False
                return
            
            if distance_to_target_length != 0:
                distance_to_target.normalize_ip()
                distance_to_target = distance_to_target * PLAYER_SPEED
                self.current_pos += distance_to_target

            self.rect.center = CellToPoint(self.current_pos, self.difficulty)
            
class Block(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.BLOCK
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)
        
class Goal(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.GOAL
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self._layer = 1
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(GOAL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class Ice(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.ICE
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(ICE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

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

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text: str, font_file: str, font_size: int, location: Point, color: tuple, anchor: str = 'center'):
        super().__init__()
        self.font = pygame.font.Font(font_file, font_size)
        self.color = color
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.anchor = anchor
        self.location = location
        if anchor == 'center':
            self.rect.center = location
        elif anchor == 'topleft':
            self.rect.topleft = location
        elif anchor == 'topright':
            self.rect.topright = location
        elif anchor == 'bottomleft':
            self.rect.bottomleft = location
        elif anchor == 'bottomright':
            self.rect.bottomright = location
        else:
            raise ValueError("Invalid anchor point")
        
    def update_text(self, text: str):
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        if self.anchor == 'center':
            self.rect.center = self.location
        elif self.anchor == 'topleft':
            self.rect.topleft = self.location
        elif self.anchor == 'topright':
            self.rect.topright = self.location
        elif self.anchor == 'bottomleft':
            self.rect.bottomleft = self.location
        elif self.anchor == 'bottomright':
            self.rect.bottomright = self.location
        else:
            raise ValueError("Invalid anchor point")

class TitleScreenPlayerSprite(pygame.sprite.Sprite):
    def __init__(self, center_location: Point):
        super().__init__()
        self.surface = pygame.Surface((100, 100))
        self.surface.fill(PLAYER_COLOR)
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.center = center_location

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