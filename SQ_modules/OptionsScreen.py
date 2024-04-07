import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from SQ_modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_TEXT_COLOR, LEFT_CLICK, TITLE_SCREEN_COLOR, GAME_VOLUME, WHITE, DARK_GRAY, TITLE_FONT, MUTE_GREEN
from SQ_modules.Sprites import TextSprite
from SQ_modules.DataTypes import Point, Size
from SQ_modules.Button import Button, SqButton
from SQ_modules.GameEnums import Screen
from SQ_modules.Metas import SqScreenMeta
from SQ_modules.NavigationManager import NavigationManager
from SQ_modules.Slider import Slider
from SQ_modules.GameAudio import GameAudio

class OptionsScreen(metaclass=SqScreenMeta):
    def __init__(self, screen):
        self.navigation_manager: NavigationManager = NavigationManager()
        self.screen = screen
        self.click_type = None


        self.title_sprite = TextSprite(
            "Options", 
            TITLE_FONT, 
            100, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//8),
            TITLE_SCREEN_TEXT_COLOR,
            outline_color=(0,0,0),
            outline_width=1
            )
        
        self.title_screen_button: SqButton = SqButton(screen, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1]//8), width=350, height=70, font_size=40, text="Title Screen")
        self.back_button: SqButton = SqButton(screen, Point(50, 50), width=50, height=50, font_size=70, text="<<")


        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)

        self.music_volume_slider = Slider(self.screen, GAME_VOLUME, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//3), DARK_GRAY, WHITE, Size(200, 5), Size(10, 20), font=TITLE_FONT, font_size=45, label='Music Volume')
        self.sfx_volume_slider = Slider(self.screen, GAME_VOLUME, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//2), DARK_GRAY, WHITE, Size(200, 5), Size(10, 20), font=TITLE_FONT, font_size=45, label='SFX Volume')

        self.game_audio = GameAudio()

    def update(self, events: list[pygame.event.Event]):
        """
        """
        self.title_screen_sprite_group.update()
        self.title_screen_button.update(events)
        self.back_button.update(events)
        self.music_volume_slider.update(events)
        self.sfx_volume_slider.update(events)
        self.game_audio.update_music_volume(self.music_volume_slider.current_slider_percent)
        self.game_audio.update_sfx_volume(self.sfx_volume_slider.current_slider_percent)


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
                    if self.back_button.is_over(event.pos):
                        if not self.navigation_manager.game_active:
                            self.navigation_manager.navigate_to(Screen.TITLE)
                        else:
                            self.navigation_manager.navigate_to(Screen.GAME)

    def draw(self):
        self.screen.fill(MUTE_GREEN)
        self.title_screen_sprite_group.draw(self.screen)
        self.title_screen_button.draw()
        self.music_volume_slider.draw()
        self.sfx_volume_slider.draw()
        self.back_button.draw()

        

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