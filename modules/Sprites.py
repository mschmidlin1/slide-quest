import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.configs import CELLSIZE, CELL_WIDTH, CELL_HEIGHT, WALL_COLOR, GOAL_COLOR, ICE_COLOR, PLAYER_COLOR, PLAYER_SPEED
from modules.Point import Point



class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    def GameboardCell_To_CenterPixelCoords(self, location: Point) -> Point:
        """
        Converts the coordinates of the Gameboard into the center pixel location of the correct cell.
        """
        x = self.border_width + (location[0] * CELL_WIDTH) + (CELL_WIDTH // 2)
        y = self.border_height + (location[1] * CELL_HEIGHT) + (CELL_HEIGHT // 2)
        return Point(round(x), round(y))
    
    #is this doing the same thing? If so, we should probably just have one method
    def GameboardPlayer_To_CenterPixelCoords(self, location: Point) -> Point:
        """
        Converts the coordinates of the Gameboard into the center pixel location of the player cell.
        """
        x = self.border_width + (location[0] * CELL_WIDTH) + (CELL_WIDTH // 2)
        y = self.border_height + (location[1] * CELL_HEIGHT) + (CELL_HEIGHT // 2)
        return Point(round(x), round(y))


class Player(Cell):
    def __init__(self, gameboard_loc: Point, border_width, border_height):
        super().__init__()
        self.border_width = border_width
        self.border_height = border_height
        self._layer = 1
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.GameboardPlayer_To_CenterPixelCoords(gameboard_loc)
        self.current_position = self.rect.center
        self.speed = PLAYER_SPEED
        self.moving = False


    def move(self, location: Point):
        """
        Set's the target position for the player as long as the player is not already moving.
        """
                                                    #make sure to change 32 into cell dimensions
        self.current_position = self.rect.centerx // 32 - self.border_width // 32, self.rect.centery // 32 - self.border_width // 32
        self.target_pos = location[0], location[1]
        
        self.current_position = pygame.Vector2(self.current_position)
        self.target_pos = pygame.Vector2(self.target_pos)

        print("Starting Position: ", self.current_position, "Target Position: ", self.target_pos)

        self.moving = True

    def update(self):
        if self.moving:
            
            self.target_pos_pixels = self.GameboardPlayer_To_CenterPixelCoords(self.target_pos)

            if self.rect.center == self.target_pos_pixels:
                self.moving = False
                return
            
            #shouldn't use 'move' as variable name and method name
            move = self.target_pos - self.current_position
            move_distance = move.length()
            
            if move_distance < self.speed:
                self.rect.center = self.target_pos_pixels #should save this as a variable since you use the value more than once
                self.moving = False
                return
            
            if move_distance != 0:
                move.normalize_ip()
                move = move * PLAYER_SPEED
                self.current_position += move 

            self.rect.center = self.GameboardPlayer_To_CenterPixelCoords(self.current_position)
            
            
class Block(Cell):
    def __init__(self, gameboard_loc: Point, border_width, border_height):
        super().__init__()
        self.border_width = border_width
        self.border_height = border_height
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.GameboardCell_To_CenterPixelCoords(gameboard_loc)
        
class Goal(Cell):
    def __init__(self, gameboard_loc: Point, border_width, border_height):
        super().__init__()
        self.border_width = border_width
        self.border_height = border_height
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(GOAL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.GameboardCell_To_CenterPixelCoords(gameboard_loc)

class Ice(Cell):
    def __init__(self, gameboard_loc: Point, border_width, border_height):
        super().__init__()
        self.border_width = border_width
        self.border_height = border_height
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(ICE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.GameboardCell_To_CenterPixelCoords(gameboard_loc)

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text: str, font_file: str, font_size: int, center_location: Point, color: tuple):
        super().__init__()
        self.font = pygame.font.Font(font_file, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = center_location



class TitleScreenPlayerSprite(pygame.sprite.Sprite):
    def __init__(self, center_location: Point):
        super().__init__()
        self.surface = pygame.Surface((100, 100))
        self.surface.fill(PLAYER_COLOR)
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.center = center_location
