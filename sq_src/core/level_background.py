import sys
import os

from sq_src.controls.rectangle import Rectangle
from sq_src.data_structures.converters import IsPointInGameboard
from sq_src.sprites.background_spites import Border
from sq_src.sprites.snow import Snow
from sq_src.sprites.text_sprite import TextSprite
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from sq_src.configs import BLACK, DARK_GRAY, NAVY_BLUE, TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR, CELL_DIMENSIONS, Border_Size_Lookup, BLUE_ICE, MUTE_GREEN
from sq_src.data_structures.game_enums import GameDifficulty
from sq_src.data_structures.data_types import Point, Anchor

class LevelBackground():
    def __init__(self, screen: pygame.surface.Surface, map_seed: str, difficulty: GameDifficulty):
        
        self.screen = screen
        self.difficulty = difficulty
        self.border_sprites = pygame.sprite.Group()
        self.bottom_border_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.map_seed = map_seed
        self.is_level_editor_on = False
        self.current_seed_sprite = TextSprite(
            f"Seed: {self.map_seed}", 
            TITLE_FONT,
            20,
            Point(10, WINDOW_DIMENSIONS.height-10),
            NAVY_BLUE, 
            anchor=Anchor.BOTTOM_LEFT)

        self.time_center_loc = Point(WINDOW_DIMENSIONS.width//2, WINDOW_DIMENSIONS.height-30)
        self.time_sprite = TextSprite(
            "", 
            TITLE_FONT,
            40,
            self.time_center_loc,
            BLACK,
            anchor=Anchor.CENTER)
        
        self.time_background_rectangle = Rectangle(
            self.screen,
            BLUE_ICE,
            Point(self.time_center_loc.x, self.time_center_loc.y+2),
            width = 100,
            height = 24,
            outline_color=DARK_GRAY,
            border_radius=5
        )
        self.solution_sprite = TextSprite(
            "",
            TITLE_FONT,
            30,
            Point(WINDOW_DIMENSIONS.width-10, WINDOW_DIMENSIONS.height-10),
            (255, 0, 0),
            anchor=Anchor.BOTTOM_RIGHT)
        
        self.time_sprite_group = pygame.sprite.Group()
        self.time_sprite_group.add(self.time_sprite)

        self.level_editor_sprites = pygame.sprite.Group()
        self.level_editor_sprites.add(self.current_seed_sprite)
        self.level_editor_sprites.add(self.solution_sprite)

        self.fill_background()
        self.load_border_sprites()

    def load_border_sprites(self):
        """Loads all the ice cliff borders into a sprite group."""
        self.border_sprites.empty()  # Clear existing sprites to avoid duplicates
        self.bottom_border_sprites.empty()

        self.border_size = Border_Size_Lookup[self.difficulty]

        border_width, border_height = self.border_size.width, self.border_size.height

        # Calculate start and end points for the border
        start_x = border_width - CELL_DIMENSIONS.width
        end_x = WINDOW_DIMENSIONS.width - (border_width - CELL_DIMENSIONS.width)
        start_y = border_height - CELL_DIMENSIONS.height
        end_y = WINDOW_DIMENSIONS.height - (border_height)

        top_left_corner = Point(start_x, start_y)
        top_left_corner_above = Point(start_x, start_y - CELL_DIMENSIONS.height)
        top_right_corner = Point(end_x - CELL_DIMENSIONS.width, start_y)
        top_right_corner_above = Point(end_x - CELL_DIMENSIONS.width, start_y - CELL_DIMENSIONS.height)
        bottom_left_corner = Point(start_x, end_y -  CELL_DIMENSIONS.height)
        bottom_right_corner = Point(end_x - CELL_DIMENSIONS.width, end_y - CELL_DIMENSIONS.height)


        self.border_sprites.add(Border(top_left_corner, 'border_topLeft'))
        self.border_sprites.add(Border(top_left_corner_above, 'border_topLeftAbove'))
        self.border_sprites.add(Border(top_right_corner, 'border_topRight'))
        self.border_sprites.add(Border(top_right_corner_above, 'border_topRightAbove'))

        self.border_sprites.add(Border(bottom_left_corner, 'border_bottomLeft'))
        self.border_sprites.add(Border(bottom_right_corner, 'border_bottomRight'))

        # Top border below
        for x in range(start_x + CELL_DIMENSIONS.width, end_x - CELL_DIMENSIONS.width, CELL_DIMENSIONS.width):
            self.border_sprites.add(Border(Point(x, start_y), 'border_top'))

        # Top border above
        for x in range(start_x + CELL_DIMENSIONS.width, end_x - CELL_DIMENSIONS.width, CELL_DIMENSIONS.width):
            self.border_sprites.add(Border(Point(x, start_y - CELL_DIMENSIONS.height), 'border_topAbove'))

        # Bottom border
        for x in range(start_x+ CELL_DIMENSIONS.width, end_x  - CELL_DIMENSIONS.width, CELL_DIMENSIONS.width):
            self.bottom_border_sprites.add(Border(Point(x, end_y - CELL_DIMENSIONS.height), 'border_bottom'))

        # Left border
        for y in range(start_y + CELL_DIMENSIONS.height, end_y  - CELL_DIMENSIONS.height, CELL_DIMENSIONS.height):
            self.border_sprites.add(Border(Point(start_x, y), 'border_left'))

        # Right border
        for y in range(start_y + CELL_DIMENSIONS.height, end_y - CELL_DIMENSIONS.height, CELL_DIMENSIONS.height):
            self.border_sprites.add(Border(Point(end_x - CELL_DIMENSIONS.width, y), 'border_right'))

        # Note: Adjust 'border_horizontal' and 'border_vertical' to your actual sprite names

    def fill_background(self):
        """Fills the area outside of the gameboard with snow."""
        for y in range(0, WINDOW_DIMENSIONS.height, CELL_DIMENSIONS.height):
            for x in range(0, WINDOW_DIMENSIONS.width, CELL_DIMENSIONS.width):
                if not IsPointInGameboard(Point(x, y), self.difficulty):
                    self.background_sprites.add(Snow(Point(x,y)))

    def update(self, time_str: str, solution: str, level_editor_on: bool):
        self.time_sprite.update_text(time_str)
        self.solution_sprite.update_text(solution)
        self.is_level_editor_on = level_editor_on
    def draw(self):
        self.border_sprites.draw(self.screen)
        self.time_background_rectangle.draw()
        self.time_sprite_group.draw(self.screen)
        if self.is_level_editor_on:
            self.level_editor_sprites.draw(self.screen)

