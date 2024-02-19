import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR
from modules.Sprites import TextSprite, Player
from modules.DataTypes import Point

class LevelCompleteScreen():
    def __init__(self, screen, num_moves: int, time_str: str, least_possible_moves: int):
        
        self.screen = screen


        self.main_menu_sprite = TextSprite(
            "Press (Esc) for main menu", 
            TITLE_FONT, 
            15, 
            Point(10, 10),
            TITLE_SCREEN_TEXT_COLOR,
            anchor='topleft')
        
        self.time_sprite = TextSprite(
            f"{time_str}", 
            TITLE_FONT, 
            15, 
            Point(WINDOW_DIMENSIONS.width-10, 10),
            TITLE_SCREEN_TEXT_COLOR,
            anchor='topright')
        
        self.title_sprite = TextSprite(
            f"Took {num_moves} moves to complete", 
            TITLE_FONT, 
            40, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1]//3-300),
            TITLE_SCREEN_TEXT_COLOR)
        
        self.best_possible_sprite = TextSprite(
            f"Best possible is {least_possible_moves} moves to complete", 
            TITLE_FONT, 
            40, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1]//3-200),
            TITLE_SCREEN_TEXT_COLOR)
        
        self.next_level_sprite = TextSprite(
            "Press (Space) to continue to next level", 
            TITLE_FONT, 
            40, 
            Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1]//3)+80),
            TITLE_SCREEN_TEXT_COLOR)


        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)
        self.title_screen_sprite_group.add(self.main_menu_sprite)
        self.title_screen_sprite_group.add(self.next_level_sprite)
        self.title_screen_sprite_group.add(self.time_sprite)
        self.title_screen_sprite_group.add(self.best_possible_sprite)

    def draw(self):
        self.screen.fill(TITLE_SCREEN_COLOR)
        self.title_screen_sprite_group.update()
        self.title_screen_sprite_group.draw(self.screen)




if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    clock = pygame.time.Clock()

    title_screen = LevelCompleteScreen(screen, num_moves=0, time_str='00:00')

    while True:
        title_screen.draw()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.flip()
        clock.tick(60)