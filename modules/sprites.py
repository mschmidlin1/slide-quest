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
        self.position = (x, y)

    def update(self):
        self.rect.x = self.x * CELLSIZE
        self.rect.y = self.y * CELLSIZE

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
    
    def updatePlayerPosition(self):
        print(self.position)

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
        

class Goal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(GOAL_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * CELLSIZE
        self.rect.y = y * CELLSIZE

class Ice(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(ICE_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * CELLSIZE
        self.rect.y = y * CELLSIZE