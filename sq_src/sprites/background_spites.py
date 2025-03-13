




import random
import numpy as np
import pygame

from sq_src.configs import Border_Size_Lookup
from sq_src.data_structures.converters import CellToPoint
from sq_src.data_structures.data_types import Cell, Point
from sq_src.data_structures.game_enums import CellType, GameDifficulty
from sq_src.data_structures.neighbors import Neighbors
from sq_src.singletons.level_manager import LevelManager
from sq_src.sprites.game_sprite import GameSprite
from sq_src.sprites.snow import GroundSnow
from sq_src.sprites.sprite_loader import SpriteLoader


class Block(GroundSnow):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty, neighbors: Neighbors, add_block_image = True):
        super().__init__(gameboard_loc, difficulty, neighbors)
        self.cellType = CellType.BLOCK
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.neighbors = neighbors
        self.level_manager = LevelManager()
        rng = np.random.RandomState(self.level_manager.current_seed.number)
        block_variants = ['block_1x1_a', 'block_1x1_b', 'block_1x1_c', 'block_1x1_d', 'block_1x1_e']
        self.chosen_block: str = rng.choice(block_variants)
        self.block_image = SpriteLoader.get_sprite(self.chosen_block)# Use the chosen sprite
        if add_block_image:
            self.image.blit(self.block_image, (self.sprite_size, self.sprite_size))
        self.editor_image = self.snow_surface.copy()
        self.editor_image.blit(self.block_image, (0, 0))
    
    def remove_block_image(self):
        """Remove the block image from the snow background."""
        self.create_snow_borders_image()

class LargeBlock(pygame.sprite.Sprite):
    def __init__(self, block_type: str, upper_left: Point):
        super().__init__()
        self.block_type = block_type
        self.upper_left = upper_left
        self.image = SpriteLoader.get_sprite(self.block_type)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.upper_left

class Goal(GroundSnow):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty, neighbors: Neighbors):
        super().__init__(gameboard_loc, difficulty, neighbors)
        self.cellType = CellType.GOAL
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.goal_image = SpriteLoader.get_sprite('goal')
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)
        self.image.blit(self.goal_image, (self.sprite_size, self.sprite_size))

        self.editor_image = self.goal_image

class Ice(GameSprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.ICE
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.image = SpriteLoader.get_sprite('ice')
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)
        self.editor_image = self.image

class Border(pygame.sprite.Sprite):
    def __init__(self, position: Point, sprite_name: str):
        super().__init__()
        self.image = SpriteLoader.get_sprite(sprite_name)
        self.rect = self.image.get_rect()
        self.rect.topleft = (position.x, position.y)



