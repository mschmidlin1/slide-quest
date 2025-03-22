import sys
import os

from sq_src.controls.rectangle import Rectangle
from sq_src.sprites.text_sprite import TextSprite
from sq_src.controls.star import Star
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from sq_src.configs import BLACK, TITLE_FONT, WHITE, WINDOW_DIMENSIONS, TITLE_SCREEN_TEXT_COLOR, LEFT_CLICK, BLUE_ICE, GRAY_BLUE, NAVY_BLUE, UGLY_PINK, MUTE_GREEN, LIGHT_BLUE, SNOWFLAKE_FONT, GOAL_COLOR, GRAY, DARK_GRAY
from sq_src.data_structures.data_types import Point, Size, Anchor
from sq_src.controls.button import Button, SqButton
from sq_src.data_structures.game_enums import Screen, GameDifficulty
from sq_src.metas import SqScreenMeta
from sq_src.singletons.navigation_manager import NavigationManager
from sq_src.singletons.level_manager import LevelManager
from sq_src.controls.faded_rectangle import FadedRectangle

class TitleScreen(metaclass=SqScreenMeta):
    def __init__(self, screen):
        
        self.navigation_manager = NavigationManager()
        self.level_manager = LevelManager()

        self.screen = screen
        self.click_type = None

        self.background_image = pygame.transform.scale(
            pygame.image.load('resources/images/mainmenu.png').convert(),
            (WINDOW_DIMENSIONS[0], WINDOW_DIMENSIONS[1])
        )

        self.faded_ellipse = FadedRectangle(self.screen, Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//5)+8), Size(850, 210), LIGHT_BLUE, 50)

        self.title_sprite = TextSprite(
            "Slide Quest!", 
            TITLE_FONT, 
            200, 
            Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//5),
            TITLE_SCREEN_TEXT_COLOR,
            outline_color=(0,0,0),
            outline_width=3
            )
        
        # Create star display in top right corner
        self.total_stars = self.level_manager.get_total_stars()
        self.star = Star(self.screen, GOAL_COLOR, Size(50, 50), 
                        (WINDOW_DIMENSIONS.width - 130, 50), 
                        outline_color=GRAY, outline_thickness=2, inner_star_thickness=0)

        # Draw rectangle behind star count for better readability
        self.stars_rect = Rectangle(self.screen, LIGHT_BLUE, Point(WINDOW_DIMENSIONS.width - 70, 50), 200, 70)   

        self.stars_text = TextSprite(
            f"x{self.total_stars}",
            TITLE_FONT,
            50,
            Point(WINDOW_DIMENSIONS.width - 100, 30),
            WHITE,
            outline_color=(0,0,0),
            outline_width=1,
            anchor=Anchor.TOP_LEFT
        )
        
        self.options_button: SqButton = SqButton(screen, Point(50, 50), width=50, height=50, font_size=40, text="F", font_file=SNOWFLAKE_FONT)
        self.tutorial_play_button: SqButton = SqButton(screen, Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//2) - 100), width=300, height=50, font_size=40, text="Tutorial", font_file=TITLE_FONT)
        self.begginer_play_button: SqButton = SqButton(screen, Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//2) + 0), width=300, height=50, font_size=40, text="Beginner", font_file=TITLE_FONT)
        self.intermediate_play_button: SqButton = SqButton(screen, Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//2) + 100), width=300, height=50, font_size=40, text="Intermediate", font_file=TITLE_FONT)
        self.hard_play_button: SqButton = SqButton(screen, Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//2) + 200), width=300, height=50, font_size=40, text="Hard", font_file=TITLE_FONT)
        self.expert_play_button: SqButton = SqButton(screen, Point(WINDOW_DIMENSIONS[0]//2, (WINDOW_DIMENSIONS[1]//2) + 300), width=300, height=50, font_size=40, text="Expert", font_file=TITLE_FONT)

        self.title_screen_sprite_group = pygame.sprite.Group()
        self.title_screen_sprite_group.add(self.title_sprite)
        self.title_screen_sprite_group.add(self.stars_text)

    def update(self, events: list[pygame.event.Event]):
        """
        """
        self.click_type = None
        self.title_screen_sprite_group.update()
        self.options_button.update(events)
        self.tutorial_play_button.update(events)
        self.begginer_play_button.update(events)
        self.intermediate_play_button.update(events)
        self.hard_play_button.update(events)
        self.expert_play_button.update(events)

        # Update total stars display
        new_total_stars = self.level_manager.get_total_stars()
        if new_total_stars != self.total_stars:
            self.total_stars = new_total_stars
            self.stars_text.update_text(f"x {self.total_stars}")

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    if self.options_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.OPTIONS)
                    if self.tutorial_play_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.TUTORIAL)
                    if self.begginer_play_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.GAME)
                        self.navigation_manager.curent_difficulty = GameDifficulty.BEGINNER
                    if self.intermediate_play_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.GAME)
                        self.navigation_manager.curent_difficulty = GameDifficulty.INTERMEDIATE
                    if self.hard_play_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.GAME)
                        self.navigation_manager.curent_difficulty = GameDifficulty.HARD
                    if self.expert_play_button.is_over(event.pos):
                        self.navigation_manager.navigate_to(Screen.GAME)
                        self.navigation_manager.curent_difficulty = GameDifficulty.EXPERT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.navigation_manager.navigate_to(Screen.GAME)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.faded_ellipse.draw()
        self.stars_rect.draw()
        self.title_screen_sprite_group.draw(self.screen)
        self.star.draw()
        self.options_button.draw()
        self.tutorial_play_button.draw()
        self.begginer_play_button.draw()
        self.intermediate_play_button.draw()
        self.hard_play_button.draw()
        self.expert_play_button.draw()


        

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