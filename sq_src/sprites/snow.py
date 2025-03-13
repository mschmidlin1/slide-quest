






import random
import numpy as np
import pygame
from sq_src.data_structures.converters import CellToPoint
from sq_src.data_structures.data_types import Cell, Point
from sq_src.data_structures.game_enums import CellType, GameDifficulty
from sq_src.data_structures.neighbors import Neighbors
from sq_src.sprites.game_sprite import GameSprite
from sq_src.sprites.sprite_loader import SpriteLoader


class GroundSnow(GameSprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty, neighbors: Neighbors):
        super().__init__()
        self.cellType = CellType.GROUND
        self.difficulty = difficulty
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.sprite_size = 32
        self.get_snow_sprites()
        self.neighbors = neighbors
        self.create_snow_borders_image()
        
        self.editor_image = self.snow_surface.copy()

    def create_snow_borders_image(self):

        self.image = pygame.Surface((self.sprite_size*3,self.sprite_size*3), pygame.SRCALPHA)

        self.image.blit(self.snow_surface, (self.sprite_size, self.sprite_size))
        top_wall = random.choice(self.snow_boundry_top_wall_options)
        if self.neighbors.top == CellType.BORDER:
            self.image.blit(top_wall, (self.sprite_size, 0))
        
        if self.neighbors.top == CellType.ICE:
            self.image.blit(self.snow_boundry_top, (self.sprite_size, 0))
        if self.neighbors.bottom == CellType.ICE:
            self.image.blit(self.snow_boundry_bottom, (self.sprite_size, self.sprite_size * 2))
        if self.neighbors.left == CellType.ICE:
            self.image.blit(self.snow_boundry_left, (0, self.sprite_size))
        if self.neighbors.right == CellType.ICE:
            self.image.blit(self.snow_boundry_right, (self.sprite_size * 2, self.sprite_size))
        
        if self.neighbors.top == CellType.ICE and self.neighbors.left == CellType.ICE and self.neighbors.top_left == CellType.ICE:
            self.image.blit(self.snow_boundry_top_left_corner, (0, 0))
        if self.neighbors.top == CellType.ICE and self.neighbors.right == CellType.ICE and self.neighbors.top_right == CellType.ICE:
            self.image.blit(self.snow_boundry_top_right_corner, (self.sprite_size * 2, 0))
        if self.neighbors.bottom == CellType.ICE and self.neighbors.left == CellType.ICE and self.neighbors.bottom_left == CellType.ICE:
            self.image.blit(self.snow_boundry_bottom_left_corner, (0, self.sprite_size * 2))
        if self.neighbors.bottom == CellType.ICE and self.neighbors.right == CellType.ICE and self.neighbors.bottom_right == CellType.ICE:
            self.image.blit(self.snow_boundry_bottom_right_corner, (self.sprite_size * 2, self.sprite_size * 2))


        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(self.gameboard_loc, self.difficulty)

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

        self.snow_boundry_top_wall_a = SpriteLoader.get_sprite('snow_boundry_top_wall_a')
        self.snow_boundry_top_wall_b = SpriteLoader.get_sprite('snow_boundry_top_wall_b')
        self.snow_boundry_top_wall_c = SpriteLoader.get_sprite('snow_boundry_top_wall_c')
        self.snow_boundry_top_wall_d = SpriteLoader.get_sprite('snow_boundry_top_wall_d')

        self.snow_boundry_top_wall_options = [self.snow_boundry_top_wall_a, self.snow_boundry_top_wall_b, self.snow_boundry_top_wall_c, self.snow_boundry_top_wall_d]

class Snow(pygame.sprite.Sprite):
    def __init__(self, position: Point):
        super().__init__()
        self.image = SpriteLoader.get_sprite('snow_center')
        self.rect = self.image.get_rect()
        self.rect.topleft = (position.x, position.y)