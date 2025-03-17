
import sys
import os

from sq_src.controls.star import Star
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sq_src.controls.rectangle import Rectangle
from sq_src.sprites.text_sprite import TextSprite

import pygame
from sq_src.configs import BLACK, BLUE_ICE, DARK_GRAY, GOAL_COLOR, GRAY, LEVEL_COMPLETE_IMAGE, TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR, LEFT_CLICK
from sq_src.data_structures.data_types import Point, Size
from sq_src.singletons.navigation_manager import NavigationManager
from sq_src.data_structures.game_enums import Screen
from sq_src.controls.button import SqButton

class LevelCompleteScreen():
    def __init__(self, screen: pygame.surface.Surface, num_moves: int, time_str: str, least_possible_moves: int, stars: int):
        self.stars = stars
        self.screen = screen
        self.navigation_manager = NavigationManager()
        self.background_image = pygame.transform.scale(
            pygame.image.load(LEVEL_COMPLETE_IMAGE).convert_alpha(),
            self.screen.get_size()
        )
        star1_inner_thickness = 3
        star2_inner_thickness = 3
        star3_inner_thickness = 3
        if self.stars > 0:
            star1_inner_thickness = 0
        if self.stars > 1:
            star2_inner_thickness = 0
        if self.stars> 2:
            star3_inner_thickness = 0
        self.star1 = Star(self.screen, GOAL_COLOR, Size(100, 100), (WINDOW_DIMENSIONS.width//2 - 150, WINDOW_DIMENSIONS.height//2 + 100), outline_color=GRAY, outline_thickness=5, inner_star_thickness=star1_inner_thickness)
        self.star2 = Star(self.screen, GOAL_COLOR, Size(100, 100), (WINDOW_DIMENSIONS.width//2, WINDOW_DIMENSIONS.height//2 + 75), outline_color=GRAY, outline_thickness=5, inner_star_thickness=star2_inner_thickness)
        self.star3 = Star(self.screen, GOAL_COLOR, Size(100, 100), (WINDOW_DIMENSIONS.width//2 + 150, WINDOW_DIMENSIONS.height//2 + 100), outline_color=GRAY, outline_thickness=5, inner_star_thickness=star3_inner_thickness)
        self.time_sprite = TextSprite(
            f"{time_str}", 
            TITLE_FONT, 
            40, 
            Point(WINDOW_DIMENSIONS.width//2, WINDOW_DIMENSIONS.height//2 + 200),
            BLACK,
            anchor='center')
        self.time_background_rectangle = Rectangle(
            self.screen,
            BLUE_ICE,
            Point(WINDOW_DIMENSIONS.width//2, WINDOW_DIMENSIONS.height//2 + 200 + 2),
            width = 100,
            height = 24,
            outline_color=DARK_GRAY,
            border_radius=5
        )
        self.moves_text_sprite = TextSprite(
            f"{num_moves}/{least_possible_moves} moves",
            TITLE_FONT,
            40,
            Point(WINDOW_DIMENSIONS.width//2, WINDOW_DIMENSIONS.height//2 + 250),
            BLACK,
            anchor='center')

        self.moves_background_rectangle = Rectangle(
            self.screen,
            BLUE_ICE,
            Point(WINDOW_DIMENSIONS.width//2, WINDOW_DIMENSIONS.height//2 + 250+2),
            width = 200,
            height = 24,
            outline_color=DARK_GRAY,
            border_radius=5
        )

        self.title_screen_button = SqButton(screen, Point(25 + 250/2, (WINDOW_DIMENSIONS[1]-50) + 0), width=250, height=50, font_size=40, text="Title Screen", font_file=TITLE_FONT)
        self.next_level_button = SqButton(screen, Point(WINDOW_DIMENSIONS[0]-25-250//2, (WINDOW_DIMENSIONS[1]-50) + 0), width=250, height=50, font_size=40, text="Next Level", font_file=TITLE_FONT)


        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.moves_text_sprite)
        self.title_screen_sprite_group.add(self.time_sprite)

    def draw(self):
        self.screen.blit(self.background_image, (0,0))
        self.time_background_rectangle.draw()
        self.moves_background_rectangle.draw()
        self.star1.draw()
        self.star2.draw()
        self.star3.draw()
        self.title_screen_sprite_group.draw(self.screen)
        self.title_screen_button.draw()
        self.next_level_button.draw()

    def update(self, events: list[pygame.event.Event]):
        """
        Handles the events for the level complete screen.
        """
        self.title_screen_sprite_group.update()
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