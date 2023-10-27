import pygame
from modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR
from modules.Sprites import TextSprite, TitleScreenPlayerSprite
from modules.Point import Point

class TitleScreen():
    def __init__(self):
        

        self.title_font = pygame.font.Font(TITLE_FONT, 100)
        self.spacebar_font = pygame.font.Font(TITLE_FONT, 40)

        self.startup_surface = pygame.Surface(WINDOW_DIMENSIONS)
        self.startup_surface.fill(TITLE_SCREEN_COLOR)
        self.title_surface = self.title_font.render("Slide Quest!", True, TITLE_SCREEN_TEXT_COLOR)
        self.spacebar_text_surface = self.spacebar_font.render("Press Space to start!", True, TITLE_SCREEN_TEXT_COLOR)

        self.title_sprite = TextSprite(self.title_surface, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//5))
        self.spacebar_sprite = TextSprite(self.spacebar_text_surface, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1]//4))

        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)
        self.title_screen_sprite_group.add(TitleScreenPlayerSprite(Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//2)))
        self.title_screen_sprite_group.add(self.spacebar_sprite)

