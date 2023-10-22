import pygame
from modules.configs import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * CELLSIZE
        self.rect.y = y * CELLSIZE

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * CELLSIZE
        self.rect.y = y * CELLSIZE

    def update(self):
        self.rect.x = self.x * CELLSIZE
        self.rect.y = self.y * CELLSIZE