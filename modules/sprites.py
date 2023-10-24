import pygame
from modules.configs import *
from modules.GameBoard import *

class Player(pygame.sprite.Sprite):
    layer = 1
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.speed = PLAYER_SPEED
        self.image = pygame.Surface((CELLSIZE, CELLSIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.moving = False
        self.x = x
        self.y = y
        self.rect.x = x * CELLSIZE
        self.rect.y = y * CELLSIZE
        self.position = pygame.Vector2(x, y)
        self.set_target(self.position)

    def set_target(self, pos) -> pygame.Vector2:
        self.target = self.target_x, self.target_y = pygame.Vector2(pos)     
        return self.target

    def update(self):
        move = self.target - self.position
        move_length = move.length()

        if move_length < self.speed:
            self.position = self.target
            self.moving = False
        elif move_length != 0:
            move.normalize_ip()
            move = move * self.speed
            self.position += move   
            self.moving = True
        
        self.rect = list(int(v * CELLSIZE) for v in self.position)

    def updatePlayerPosition(self):
        print(self.position)

class Wall(pygame.sprite.Sprite):
    layer = 0
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
    layer = 0
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
    layer = 0
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