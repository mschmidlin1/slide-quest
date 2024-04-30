import pygame
from sq_src.singletons.user_data import UserData
from sq_src.configs import MUTE_GREEN, WHITE, BLUE_ICE, WINDOW_DIMENSIONS, TITLE_FONT, LEFT_CLICK
from sq_src.data_structures.data_types import Point, Size
from sq_src.controls.text_box import TextBox
from sq_src.singletons.navigation_manager import NavigationManager
from sq_src.data_structures.game_enums import Screen
from sq_src.controls.button import SqButton
from sq_src.screens.options_screen import OptionsScreen


class WelcomeScreen:
    def __init__(self, screen):
        self.user_data = UserData()
        self.navigation_manager = NavigationManager()
        self.screen = screen
        self.font_size = 32
        self.font = pygame.font.Font(None, self.font_size)
        self.font_color = pygame.Color('white')
        self.welcome_text = "Welcome! Please enter a user name:"
        self.text_surface = self.font.render(self.welcome_text, True, self.font_color)

        self.center_pos = Point(WINDOW_DIMENSIONS.width//2, WINDOW_DIMENSIONS.height//2)
        self.text_surface_rect = self.text_surface.get_rect()
        self.width = self.text_surface_rect.width
        self.textbox = TextBox(center=Point(self.center_pos.x, self.center_pos.y+100), size=Size(width=self.width, height=50), font_size=self.font_size, color_active=BLUE_ICE, color_inactive=WHITE)


        self.apply_button = SqButton(self.screen, Point(self.center_pos.x, self.center_pos.y+200), width=100, height=60, text='Apply', font_file=TITLE_FONT, font_size=40)
    def draw(self):
        self.screen.fill(MUTE_GREEN)
        self.screen.blit(self.text_surface, (self.center_pos.x-self.width//2, self.center_pos.y-self.text_surface_rect.height))
        self.textbox.draw(self.screen)
        self.apply_button.draw()
    
    def handle_username_apply(self):
            self.navigation_manager.navigate_to(Screen.TITLE)
            user_name = self.textbox.text.strip()
            self.user_data.set_user_name(user_name)
            options_screen = OptionsScreen()
            options_screen.user_name_text_box.text = user_name
            options_screen.user_name_sprite.update_text(user_name)

    def update(self, events):
        self.textbox.update(events)
        self.apply_button.update(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.handle_username_apply()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    if self.apply_button.is_over(event.pos):
                        self.handle_username_apply()