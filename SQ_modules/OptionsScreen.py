import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from SQ_modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_TEXT_COLOR, LEFT_CLICK, TITLE_SCREEN_COLOR
from SQ_modules.Sprites import TextSprite
from SQ_modules.DataTypes import Point, Size
from SQ_modules.Button import Button
from SQ_modules.GameEnums import Screen
from SQ_modules.Metas import SqScreenMeta
from SQ_modules.NavigationManager import NavigationManager
from SQ_modules.Slider import Slider

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
        
        self.title_screen_button: Button = Button(screen, (255,255,255), x=600, y=600, width=200, height=100, text="Title Screen", hover_color=(0,255,255))

        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)

        self.volume_slider = Slider(self.screen, Point(500, 500), (255, 0, 255), (255, 0, 0), Size(200, 5), Size(10, 20), label='volume slider')

    def update(self, events: list[pygame.event.Event]):
        """
        """
        self.title_screen_sprite_group.update()
        self.title_screen_button.update(events)
        self.volume_slider.update(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.navigation_manager.game_active:
                        self.navigation_manager.navigate_to(Screen.TITLE)
                    else:
                        self.navigation_manager.navigate_to(Screen.GAME)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    if self.title_screen_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.TITLE)

    def draw(self):
        self.screen.fill(TITLE_SCREEN_COLOR)
        self.title_screen_sprite_group.draw(self.screen)
        self.title_screen_button.draw()
        self.volume_slider.draw()

        

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