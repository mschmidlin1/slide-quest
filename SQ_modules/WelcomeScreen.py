import pygame
from SQ_modules.configs import MUTE_GREEN, WHITE, BLUE_ICE, WINDOW_DIMENSIONS
from SQ_modules.DataTypes import Point, Size
from SQ_modules.TextBox import TextBox
from SQ_modules.NavigationManager import NavigationManager
from SQ_modules.GameEnums import Screen


class WelcomeScreen:
    def __init__(self, screen):
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

    def draw(self):
        self.screen.fill(MUTE_GREEN)
        self.screen.blit(self.text_surface, (self.center_pos.x-self.width//2, self.center_pos.y-self.text_surface_rect.height))
        self.textbox.draw(self.screen)

    def update(self, events):
        self.textbox.update(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.navigation_manager.navigate_to(Screen.TITLE)