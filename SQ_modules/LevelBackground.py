import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from SQ_modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR, CELL_DIMENSIONS, Border_Size_Lookup
from SQ_modules.Sprites import TextSprite, SpriteLoader, Border, Background
from SQ_modules.GameEnums import GameDifficulty
from SQ_modules.DataTypes import Point

class LevelBackground():
    def __init__(self, screen: pygame.surface.Surface, text: str, difficulty: GameDifficulty):
        
        self.screen = screen
        self.difficulty = difficulty
        self.border_sprites = pygame.sprite.Group()
        self.bottom_border_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()

        self.main_menu_sprite = TextSprite(
            "Press (Esc) for main menu", 
            TITLE_FONT, 
            15, 
            Point(10, 10),
            TITLE_SCREEN_TEXT_COLOR,
            anchor='topleft')

        self.current_level_sprite = TextSprite(
            f"{text}", 
            TITLE_FONT,
            15,
            Point(WINDOW_DIMENSIONS.width//2, 10),
            TITLE_SCREEN_TEXT_COLOR, 
            anchor='center')
        
        self.time_sprite = TextSprite(
            "", 
            TITLE_FONT,
            15,
            Point(WINDOW_DIMENSIONS.width-10, 10),
            TITLE_SCREEN_TEXT_COLOR,
            anchor='topright')
        
        self.solution_sprite = TextSprite(
            "",
            TITLE_FONT,
            15,
            Point(WINDOW_DIMENSIONS.width-10, WINDOW_DIMENSIONS.height-10),
            TITLE_SCREEN_TEXT_COLOR,
            anchor='bottomright')
        
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.current_level_sprite)
        self.sprite_group.add(self.time_sprite)
        self.sprite_group.add(self.main_menu_sprite)
        self.sprite_group.add(self.solution_sprite)

    def load_border_sprites(self):
        # Ensure this method is called once or in a way that doesn't keep adding sprites on each draw call
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
        for y in range(0, WINDOW_DIMENSIONS.height, CELL_DIMENSIONS.height):
            for x in range(0, WINDOW_DIMENSIONS.width, CELL_DIMENSIONS.width):
                self.background_sprites.add(Background(Point(x,y)))

    def draw(self, time_str: str, solution: str):
        self.load_border_sprites()  # Make sure to call this to load and place border sprites
        self.border_sprites.draw(self.screen)  # Draw the border sprites
        self.time_sprite.update_text(time_str)
        self.solution_sprite.update_text(solution)
        self.sprite_group.draw(self.screen)

if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    clock = pygame.time.Clock()

    level_background = LevelBackground(screen, "This is the level name")

    while True:
        level_background.draw()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)