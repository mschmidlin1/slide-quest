import pygame
import sys
from modules.Game import Game
from modules.configs import (
    WINDOW_DIMENSIONS, 
    WINDOW_TITLE, 
    CURRENT_DIFFICULTY
)
from modules.Point import Point
from modules.TitleScreen import TitleScreen
from modules.GameEnums import GameDifficulty


if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    title_screen = TitleScreen()

    current_game = None
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_game==None:
                    current_game = Game(CURRENT_DIFFICULTY, screen)
        
        if current_game!=None:
            if current_game.isComplete():
                current_game = None
            else:
                current_game.update(events)

        if current_game==None:
            screen.blit(title_screen.startup_surface, (0,0))
            title_screen.title_screen_sprite_group.update()
            title_screen.title_screen_sprite_group.draw(screen)


        pygame.display.flip()