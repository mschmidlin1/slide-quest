import sys
import os

from sq_src.singletons.banner_manager import BannerManager
from sq_src.singletons.level_manager import LevelManager
from sq_src.sprites.text_sprite import TextSprite
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from sq_src.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_TEXT_COLOR, LEFT_CLICK, TITLE_SCREEN_COLOR, WHITE, DARK_GRAY, TITLE_FONT, MUTE_GREEN, BLUE_ICE
from sq_src.data_structures.data_types import Point, Size
from sq_src.controls.button import Button, SqButton
from sq_src.data_structures.game_enums import Screen
from sq_src.metas import SqScreenMeta, SingletonMeta
from sq_src.singletons.navigation_manager import NavigationManager
from sq_src.controls.slider import Slider
from sq_src.singletons.game_audio import GameAudio
from sq_src.singletons.user_data import UserData
from sq_src.controls.text_box import TextBox

class OptionsScreen(metaclass=SingletonMeta):
    """
    This class represents the options screen in a game. It handles user interactions related
    to modifying game settings such as music volume, sound effects volume, and user name.
    """
    def __init__(self, screen: pygame.surface.Surface):
        self.navigation_manager: NavigationManager = NavigationManager()
        self.screen = screen
        self.click_type = None
        self.user_data = UserData()
        self.game_audio = GameAudio()
        self.banner_manager = BannerManager()

        self.title_sprite = TextSprite(
            "Options", 
            TITLE_FONT, 
            100, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//8),
            TITLE_SCREEN_TEXT_COLOR,
            outline_color=(0,0,0),
            outline_width=1
            )
        

        self.user_name_sprite = TextSprite(
            self.user_data.get_user_name(),
            TITLE_FONT,
            35,
            Point(WINDOW_DIMENSIONS.width-20, 20),
            TITLE_SCREEN_TEXT_COLOR,
            outline_color=(0,0,0),
            outline_width=1,
            anchor='topright'
            )
        

        self.edit_name_sprite = TextSprite(
            "Edit your user name:",
            TITLE_FONT,
            35,
            Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//2)+140),
            TITLE_SCREEN_TEXT_COLOR,
            outline_color=(0,0,0),
            outline_width=1,
            anchor='center'
            )


        self.user_name_text_box = TextBox(Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//2)+200), Size(width=200, height=50),  font_size=32, color_active=BLUE_ICE, color_inactive=WHITE, active_by_default=False)
        self.user_name_text_box.text = self.user_data.get_user_name()
        
        self.title_screen_button: SqButton = SqButton(screen, Point(150, WINDOW_DIMENSIONS[1] - 60), width=250, height=60, font_size=40, text="Title Screen")
        self.back_button: SqButton = SqButton(screen, Point(50, 50), width=50, height=50, font_size=70, text="<<")
        self.apply_button = SqButton(self.screen, Point(WINDOW_DIMENSIONS[0]-75, (WINDOW_DIMENSIONS[1]//2)+200), width=100, height=60, text='Apply', font_file=TITLE_FONT, font_size=40)


        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)
        self.title_screen_sprite_group.add(self.user_name_sprite)
        self.title_screen_sprite_group.add(self.edit_name_sprite)

        self.music_volume_slider = Slider(self.screen, self.game_audio.current_music_volume, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//3), DARK_GRAY, WHITE, Size(200, 5), Size(10, 20), font=TITLE_FONT, font_size=45, label='Music Volume')
        self.sfx_volume_slider = Slider(self.screen, self.game_audio.current_sfx_volume, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//2), DARK_GRAY, WHITE, Size(200, 5), Size(10, 20), font=TITLE_FONT, font_size=45, label='SFX Volume')

    def update(self, events: list[pygame.event.Event]):
        """
        Handles all update events for the options screen.
        """
        #update all child elements
        self.user_name_text_box.update(events)
        self.apply_button.update(events)
        self.title_screen_sprite_group.update()
        self.title_screen_button.update(events)
        self.back_button.update(events)
        self.music_volume_slider.update(events)
        self.sfx_volume_slider.update(events)


        #handle if the game audio is changed
        if self.game_audio.current_music_volume != self.music_volume_slider.current_slider_percent:
            self.game_audio.update_music_volume(self.music_volume_slider.current_slider_percent)
            self.user_data.update_music_volume(self.music_volume_slider.current_slider_percent)
        
        if self.game_audio.current_sfx_volume != self.sfx_volume_slider.current_slider_percent:
            self.game_audio.update_sfx_volume(self.sfx_volume_slider.current_slider_percent)
            self.user_data.update_sfx_volume(self.sfx_volume_slider.current_slider_percent)

        #handle navigation and button clicks
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
                    if self.apply_button.is_over(event.pos):
                        self.banner_manager.add_banner("User name updated!", 5, font_size=26)
                        self.user_data.set_user_name(self.user_name_text_box.text.strip())
                        self.user_name_sprite.update_text(self.user_name_text_box.text.strip())
                        self.user_name_text_box.disable()

    def draw(self):
        """
        Handles all the drawing for the options screen.
        """
        self.screen.fill(MUTE_GREEN)
        self.title_screen_sprite_group.draw(self.screen)
        self.title_screen_button.draw()
        self.music_volume_slider.draw()
        self.sfx_volume_slider.draw()
        self.back_button.draw()
        self.user_name_text_box.draw(self.screen)
        self.apply_button.draw()

        

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