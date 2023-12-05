import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.GameEnums import CellType
from modules.configs import CELL_DIMENSIONS, WALL_COLOR, GOAL_COLOR, ICE_COLOR, PLAYER_COLOR, PLAYER_SPEED
from modules.DataTypes import Point, Size



class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    def GameboardCell_To_CenterPixelCoords(self, location: Point) -> Point:
        """
        Converts the coordinates of the Gameboard into the center pixel location of the correct cell.
        """
        x = self.border_size.width + (location[0] * CELL_DIMENSIONS.width) + (CELL_DIMENSIONS.width // 2)
        y = self.border_size.height + (location[1] * CELL_DIMENSIONS.height) + (CELL_DIMENSIONS.height // 2)
        return Point(round(x), round(y))
    
    def Get_Cell_Current_Position(self, location: Point) -> Point:
        return location[0] // CELL_DIMENSIONS.width - self.border_size.width // CELL_DIMENSIONS.width, location[1] // CELL_DIMENSIONS.height - self.border_size.height // CELL_DIMENSIONS.height

class Player(Cell):
    def __init__(self, gameboard_loc: Point, border_size: Size):
        super().__init__()
        self.cellType = CellType.PLAYER
        self.border_size = border_size
        self._layer = 2
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.GameboardCell_To_CenterPixelCoords(gameboard_loc)
        self.current_pos = self.rect.center
        self.speed = PLAYER_SPEED
        self.moving = False

    def move(self, location: Point):
        """
        Set's the target position for the player as long as the player is not already moving.
        """
        self.current_pos = self.Get_Cell_Current_Position(self.rect.center)
        self.target_pos = location[0], location[1]
        
        self.current_pos = pygame.Vector2(self.current_pos)
        self.target_pos = pygame.Vector2(self.target_pos)

        print("Starting Position: ", self.current_pos, "Target Position: ", self.target_pos)

        self.moving = True

    def update(self):
        if self.moving:
            
            self.target_pos_pixels = self.GameboardCell_To_CenterPixelCoords(self.target_pos)

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

            self.rect.center = self.GameboardCell_To_CenterPixelCoords(self.current_pos)
            
class Block(Cell):
    def __init__(self, gameboard_loc: Point, border_size: Size):
        super().__init__()
        self.cellType = CellType.BLOCK
        self.border_size = border_size
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.GameboardCell_To_CenterPixelCoords(gameboard_loc)
        
class Goal(Cell):
    def __init__(self, gameboard_loc: Point, border_size: Size):
        super().__init__()
        self.cellType = CellType.GOAL
        self.border_size = border_size
        self._layer = 1
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(GOAL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.GameboardCell_To_CenterPixelCoords(gameboard_loc)

class Ice(Cell):
    def __init__(self, gameboard_loc: Point, border_size: Size):
        super().__init__()
        self.cellType = CellType.ICE
        self.border_size = border_size
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(ICE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.GameboardCell_To_CenterPixelCoords(gameboard_loc)

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text: str, font_file: str, font_size: int, center_location: Point, color: tuple):
        super().__init__()
        self.font = pygame.font.Font(font_file, font_size)
        self.color = color
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = center_location
    
    def update_text(self, text: str):
        self.image = self.font.render(text, True, self.color)

class TitleScreenPlayerSprite(pygame.sprite.Sprite):
    def __init__(self, center_location: Point):
        super().__init__()
        self.surface = pygame.Surface((100, 100))
        self.surface.fill(PLAYER_COLOR)
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.center = center_location