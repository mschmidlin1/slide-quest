import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from SQ_modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR, LEFT_CLICK
from SQ_modules.Sprites import TextSprite
from SQ_modules.DataTypes import Point
from SQ_modules.NavigationManager import NavigationManager
from SQ_modules.GameEnums import Screen
from SQ_modules.Button import SqButton

class LevelCompleteScreen():
    def __init__(self, screen, num_moves: int, time_str: str, least_possible_moves: int):
        
        self.screen = screen
        self.navigation_manager = NavigationManager()
        
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

        self.title_screen_button = SqButton(screen, Point(25 + 250/2, (WINDOW_DIMENSIONS[1]-50) + 0), width=250, height=50, font_size=40, text="Title Screen", font_file=TITLE_FONT)
        self.next_level_button = SqButton(screen, Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//2) + 100), width=250, height=50, font_size=40, text="Next Level", font_file=TITLE_FONT)


        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)
        self.title_screen_sprite_group.add(self.time_sprite)
        self.title_screen_sprite_group.add(self.best_possible_sprite)

    def draw(self):
        self.screen.fill(TITLE_SCREEN_COLOR)
        self.title_screen_sprite_group.update()
        self.title_screen_sprite_group.draw(self.screen)
        self.title_screen_button.draw()
        self.next_level_button.draw()

    def update(self, events: list[pygame.event.Event]):
        """
        Handles the events for the level complete screen.
        """
        self.title_screen_button.update(events)
        self.next_level_button.update(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.navigation_manager.navigate_to(Screen.GAME)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    if self.title_screen_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.TITLE)
                    if self.next_level_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.GAME)




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