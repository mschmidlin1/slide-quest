import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR
from modules.Sprites import TextSprite, Player
from modules.DataTypes import Point

class TitleScreen():
    def __init__(self, screen):
        
        self.screen = screen


        self.title_sprite = TextSprite(
            "Slide Quest!", 
            TITLE_FONT, 
            100, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//5),
            TITLE_SCREEN_TEXT_COLOR)
        
        self.start_sprite = TextSprite(
            "Press space to start.", 
            TITLE_FONT, 
            40, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1]//4),
            TITLE_SCREEN_TEXT_COLOR)

        self.player_sprite = Player(
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//2),
            0,
            0,
        )
        self.player_sprite.rect.center = Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//2)

        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)
        self.title_screen_sprite_group.add(self.start_sprite)
        self.title_screen_sprite_group.add(self.player_sprite)



    def draw(self):
        self.screen.fill(TITLE_SCREEN_COLOR)
        self.title_screen_sprite_group.update()
        self.title_screen_sprite_group.draw(self.screen)


if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    clock = pygame.time.Clock()

    title_screen = TitleScreen(screen)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.flip()
        clock.tick(60)