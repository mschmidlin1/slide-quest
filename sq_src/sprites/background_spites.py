




import random
import pygame

from sq_src.configs import Border_Size_Lookup
from sq_src.data_structures.converters import CellToPoint
from sq_src.data_structures.data_types import Cell, Point
from sq_src.data_structures.game_enums import CellType, GameDifficulty
from sq_src.data_structures.neighbors import Neighbors
from sq_src.sprites.sprite_loader import SpriteLoader


class Block(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty, neighbors: Neighbors):
        super().__init__()
        self.cellType = CellType.BLOCK
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        block_variants = ['block_1x1_a', 'block_1x1_b', 'block_1x1_c', 'block_1x1_d', 'block_1x1_e']
        chosen_block = random.choice(block_variants)


        block_image = SpriteLoader.get_sprite(chosen_block)# Use the chosen sprite

        self.get_snow_sprites()


        self.image = pygame.Surface((32*3,32*3), pygame.SRCALPHA)



        sprite_size = 32  # Assuming all sprites are 32x32

        self.image.blit(self.snow_surface, (sprite_size, sprite_size))
        self.image.blit(block_image, (sprite_size, sprite_size))
        
        if neighbors.top == CellType.ICE:
            self.image.blit(self.snow_boundry_top, (sprite_size, 0))
        if neighbors.bottom == CellType.ICE:
            self.image.blit(self.snow_boundry_bottom, (sprite_size, sprite_size * 2))
        if neighbors.left == CellType.ICE:
            self.image.blit(self.snow_boundry_left, (0, sprite_size))
        if neighbors.right == CellType.ICE:
            self.image.blit(self.snow_boundry_right, (sprite_size * 2, sprite_size))
        
        if neighbors.top == CellType.ICE and neighbors.left == CellType.ICE:
            self.image.blit(self.snow_boundry_top_left_corner, (0, 0))
        if neighbors.top == CellType.ICE and neighbors.right == CellType.ICE:
            self.image.blit(self.snow_boundry_top_right_corner, (sprite_size * 2, 0))
        if neighbors.bottom == CellType.ICE and neighbors.left == CellType.ICE:
            self.image.blit(self.snow_boundry_bottom_left_corner, (0, sprite_size * 2))
        if neighbors.bottom == CellType.ICE and neighbors.right == CellType.ICE:
            self.image.blit(self.snow_boundry_bottom_right_corner, (sprite_size * 2, sprite_size * 2))


        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)
    def get_snow_sprites(self):
        """ 
        """
        self.snow_surface = SpriteLoader.get_sprite('snow_center')
        self.snow_boundry_top = SpriteLoader.get_sprite('snow_boundry_top')
        self.snow_boundry_bottom = SpriteLoader.get_sprite('snow_boundry_bottom')
        self.snow_boundry_left = SpriteLoader.get_sprite('snow_boundry_left')
        self.snow_boundry_right = SpriteLoader.get_sprite('snow_boundry_right')
        self.snow_boundry_top_left_corner = SpriteLoader.get_sprite('snow_boundry_top_left_corner')
        self.snow_boundry_top_right_corner = SpriteLoader.get_sprite('snow_boundry_top_right_corner')
        self.snow_boundry_bottom_left_corner = SpriteLoader.get_sprite('snow_boundry_bottom_left_corner')
        self.snow_boundry_bottom_right_corner = SpriteLoader.get_sprite('snow_boundry_bottom_right_corner')

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



