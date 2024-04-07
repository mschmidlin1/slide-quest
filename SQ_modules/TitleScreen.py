import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from SQ_modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_TEXT_COLOR, LEFT_CLICK, BLUE_ICE, GRAY_BLUE, NAVY_BLUE, UGLY_PINK, MUTE_GREEN, LIGHT_BLUE, SNOWFLAKE_FONT
from SQ_modules.Sprites import TextSprite
from SQ_modules.DataTypes import Point
from SQ_modules.Button import Button, SqButton
from SQ_modules.GameEnums import Screen
from SQ_modules.Metas import SqScreenMeta
from SQ_modules.NavigationManager import NavigationManager

class TitleScreen(metaclass=SqScreenMeta):
    def __init__(self, screen):
        
        self.navigation_manager = NavigationManager()

        self.screen = screen
        self.click_type = None

        self.background_image = pygame.transform.scale(
            pygame.image.load('resources/images/mainmenu.png').convert(),
            (WINDOW_DIMENSIONS[0], WINDOW_DIMENSIONS[1])
        )

        self.title_sprite = TextSprite(
            "Slide Quest!", 
            TITLE_FONT, 
            100, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//5),
            TITLE_SCREEN_TEXT_COLOR,
            outline_color=(0,0,0),
            outline_width=1
            )
        
        self.options_button: SqButton = SqButton(screen, Point(50, 50), width=50, height=50, font_size=40, text="F", font_file=SNOWFLAKE_FONT)
        
        self.start_sprite = TextSprite(
            "Press space to start.", 
            TITLE_FONT, 
            40, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1]//4),
            TITLE_SCREEN_TEXT_COLOR,
            outline_color=(0,0,0),
            outline_width=1
            )

        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)
        self.title_screen_sprite_group.add(self.start_sprite)

    def update(self, events: list[pygame.event.Event]):
        """
        """
        self.click_type = None
        self.title_screen_sprite_group.update()
        self.options_button.update(events)


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    if self.options_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.OPTIONS)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.navigation_manager.navigate_to(Screen.GAME)


    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.title_screen_sprite_group.draw(self.screen)
        self.options_button.draw()
        

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