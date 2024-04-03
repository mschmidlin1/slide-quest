import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from SQ_modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_TEXT_COLOR, LEFT_CLICK, TITLE_SCREEN_COLOR
from SQ_modules.Sprites import TextSprite
from SQ_modules.DataTypes import Point
from SQ_modules.Button import Button
from SQ_modules.GameEnums import Screen
from SQ_modules.Metas import SqScreenMeta
from SQ_modules.NavigationManager import NavigationManager

class OptionsScreen(metaclass=SqScreenMeta):
    def __init__(self, screen):
        self.navigation_manager: NavigationManager = NavigationManager()
        self.screen = screen
        self.click_type = None


        self.title_sprite = TextSprite(
            "Options Yay!", 
            TITLE_FONT, 
            100, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//5),
            TITLE_SCREEN_TEXT_COLOR,
            outline_color=(0,0,0),
            outline_width=1
            )
        
        

        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)

    def update(self, events: list[pygame.event.Event]):
        """
        """
        self.title_screen_sprite_group.update()

        for event in events:
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == LEFT_CLICK:
            #         if self.options_button.is_over(event.pos):
            #             self.navigation_manager.navigate_to_options()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.navigation_manager.current_game is None:
                        self.navigation_manager.navigate_to(Screen.TITLE)
                    else:
                        self.navigation_manager.navigate_to(Screen.GAME)


    def draw(self):
        self.screen.fill(TITLE_SCREEN_COLOR)
        self.title_screen_sprite_group.draw(self.screen)
        

if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    clock = pygame.time.Clock()

    title_screen = OptionsScreen(screen)

    while True:
        title_screen.draw()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)