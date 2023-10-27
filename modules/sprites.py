import pygame
# from modules.configs import *
# from modules.GameBoard import *
from modules.configs import CELLSIZE, CELL_WIDTH, CELL_HEIGHT, WALL_COLOR, GOAL_COLOR, ICE_COLOR, PLAYER_COLOR, PLAYER_SPEED
from modules.Point import Point



class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    def GameboardCell_To_CenterPixelCoords(self, location: Point) -> Point:
        """
        Converts the coordinates of the Gameboard into the center pixel location of the correct cell.
        """
        x = self.border_width + (location.x*CELL_WIDTH) + (CELL_WIDTH//2)
        y = self.border_height + (location.y*CELL_HEIGHT) + (CELL_HEIGHT//2)
        return Point(x, y)


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
        self.rect.center = self.GameboardCell_To_CenterPixelCoords(gameboard_loc)

        self.speed = PLAYER_SPEED
        self.moving = False


    def move(self, location: Point):
        """
        Set's the target position for the player as long as the player is not already moving.
        """
        if self.moving==False:
            self.target_pos = self.GameboardCell_To_CenterPixelCoords(location)
            self.moving=True

    def update(self):
        if self.moving:
            distance = pygame.Vector2((self.target_pos[0] - self.rect.center[0], self.target_pos[1] - self.rect.center[1]))
            if distance == pygame.Vector2(0, 0):
                self.moving=False
                return
            distance.normalize_ip()
            distance = distance * self.speed
            sprite_center = pygame.Vector2(self.rect.center)
            new_center = sprite_center + distance
            self.rect.center = new_center

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
    def __init__(self, text_surface: pygame.Surface, center_location: Point):
        super().__init__()
        self.image = text_surface
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