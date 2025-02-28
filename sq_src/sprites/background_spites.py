




import random
import pygame

from sq_src.configs import Border_Size_Lookup
from sq_src.data_structures.converters import CellToPoint
from sq_src.data_structures.data_types import Cell, Point
from sq_src.data_structures.game_enums import CellType, GameDifficulty
from sq_src.sprites.sprite_loader import SpriteLoader


class Block(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.BLOCK
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        block_variants = ['block_1x1_a', 'block_1x1_b', 'block_1x1_c', 'block_1x1_d', 'block_1x1_e']
        chosen_block = random.choice(block_variants)
        block_image = SpriteLoader.get_sprite('ice').copy()
        block_image.blit(SpriteLoader.get_sprite(chosen_block), (0,0))# Use the chosen sprite
        self.image = block_image
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class Ground(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.GROUND
        self.difficulty = difficulty
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = SpriteLoader.get_sprite('background')
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class Goal(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.GOAL
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.image = SpriteLoader.get_sprite('goal')
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class Ice(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.ICE
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.image = SpriteLoader.get_sprite('ice')
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class Border(pygame.sprite.Sprite):
    def __init__(self, position: Point, sprite_name: str):
        super().__init__()
        self.image = SpriteLoader.get_sprite(sprite_name)
        self.rect = self.image.get_rect()
        self.rect.topleft = (position.x, position.y)

class Background(pygame.sprite.Sprite):
    def __init__(self, position: Point):
        super().__init__()
        self.image = SpriteLoader.get_sprite('background')
        self.rect = self.image.get_rect()
        self.rect.topleft = (position.x, position.y)



