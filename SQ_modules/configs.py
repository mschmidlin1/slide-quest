import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SQ_modules.GameEnums import GameDifficulty
from SQ_modules.DataTypes import Size
import pygame

SPRITE_POSITIONS = {
    'ice': (32, 192, 32, 32),            
    'goal': (96, 224, 32, 32),
    'background': (32, 32, 32, 32),
    'block_1x1_a': (32, 320, 32, 32),
    'block_1x1_b': (32, 352, 32, 32),
    'block_1x1_c': (64, 352, 32, 32),
    'block_1x1_d': (96, 352, 32, 32),
    'block_1x1_e': (128, 352, 32, 32),
    'border_top': (32, 128, 32, 32),
    'border_topAbove': (32, 256, 32, 32),
    'border_left': (64, 32, 32, 32),
    'border_right': (0, 32, 32, 32),
    'border_bottom': (512, 384, 32, 32),
    'border_topLeft': (64, 32, 32, 32),
    'border_topLeftAbove': (0, 256, 32, 32),
    'border_topRight': (0, 32, 32, 32),
    'border_topRightAbove': (32, 288, 32, 32),
    'border_bottomLeft': (448, 384, 32, 32),
    'border_bottomRight': (576, 384, 32, 32)
}

#choose to turn of splash screen or not
SPLASH_SCREEN_ON: bool = True

#Audio settings
GAME_VOLUME = 0.2 #0-1

#logging settings
FILE_LOG_LEVEL = "DEBUG"
STDOUT_LOG_LEVEL = "INFO"

#game settings
WINDOW_TITLE = "Slide Quest"
ICON = pygame.image.load('resources/images/Icy-Q-nobackground64x64.png')
TITLE_FONT = "resources/fonts/m5x7.otf"
PLAYER_SPRITE_SHEET = 'resources/sprites/player/Character spritesheet.png'
PLAYERSHADOW_SPRITE_SHEET = 'resources/sprites/player/player-shadow.png'
ENVIRONMENT_SPRITE_SHEET = 'resources/sprites/environment/Spritesheet_revised_2.0.png'
SNOWFLAKE_FONT = 'resources/fonts/KR Kinda Flakey.ttf'

#window information
WINDOW_DIMENSIONS = Size(width=960, height=960) #must be set to a multiple of 64
CELL_DIMENSIONS = Size(width=32,  height=32)
BEGINNER_DIMENSIONS = Size(width=12, height=12)
INTERMEDIATE_DIMENSIONS = Size(width=18, height=18)
HARD_DIMENSIONS = Size(width=22, height=22)
EXPERT_DIMENSIONS = Size(width=26, height=26)
TEST_DIMENSIONS = Size(width=10, height=10)

def calculate_border(board_dimensions: Size, window_dimensions: Size, cell_dimensions: Size) -> Size:
        """
        Given the sizes of the gameboard, the window, and how big each cell is, this function calculates and returns the size of the border regions around the gameboard.
        """
        return Size(
                width=(window_dimensions.width - (board_dimensions.width*cell_dimensions.width))//2,
                height=(window_dimensions.height - (board_dimensions.height*cell_dimensions.height))//2)


BEGINNER_BORDER = calculate_border(BEGINNER_DIMENSIONS, WINDOW_DIMENSIONS, CELL_DIMENSIONS)
INTERMEDIATE_BORDER = calculate_border(INTERMEDIATE_DIMENSIONS, WINDOW_DIMENSIONS, CELL_DIMENSIONS)
HARD_BORDER = calculate_border(HARD_DIMENSIONS, WINDOW_DIMENSIONS, CELL_DIMENSIONS)
EXPERT_BORDER = calculate_border(EXPERT_DIMENSIONS, WINDOW_DIMENSIONS, CELL_DIMENSIONS)
TEST_BORDER = calculate_border(TEST_DIMENSIONS, WINDOW_DIMENSIONS, CELL_DIMENSIONS)

Border_Size_Lookup = {
        GameDifficulty.BEGINNER: BEGINNER_BORDER,
        GameDifficulty.INTERMEDIATE: INTERMEDIATE_BORDER,
        GameDifficulty.HARD: HARD_BORDER,
        GameDifficulty.EXPERT: EXPERT_BORDER,
        GameDifficulty.TEST: TEST_BORDER
}

Board_Size_Lookup = {
        GameDifficulty.BEGINNER: BEGINNER_DIMENSIONS,
        GameDifficulty.INTERMEDIATE: INTERMEDIATE_DIMENSIONS,
        GameDifficulty.HARD: HARD_DIMENSIONS,
        GameDifficulty.EXPERT: EXPERT_DIMENSIONS,
        GameDifficulty.TEST: TEST_DIMENSIONS
}

Difficulty_Lookup: dict[Size, GameDifficulty] = {value: key for key, value in Board_Size_Lookup.items()}

#Defaul to edit on or edit off
IS_EDIT_ON_DEFAULT = False

#define colors
TITLE_SCREEN_COLOR = (37, 150, 190)
TITLE_SCREEN_TEXT_COLOR = (255, 255, 255)
BGCOLOR = (140, 140, 140)
WHITE = (255, 255, 255)
PLAYER_COLOR = (123, 5, 75)
WALL_COLOR = (2, 100, 75)
GOAL_COLOR = (255, 255, 0)
GROUND_COLOR = (88, 57, 39)
ICE_COLOR = (173, 216, 230)
PALLET_HIGHLIGHT_COLOR = (230, 237, 28)
DARK_GRAY = (43, 45, 47)
NAVY_BLUE = (11, 42, 81)
GRAY_BLUE = (47, 86, 122)
LIGHT_BLUE = (67, 184, 214)
MUTE_GREEN = (42, 77, 90)
UGLY_PINK = (175, 115, 130)
BLUE_ICE = (158, 227, 231)


#other constants
PLAYER_SPEED = .4
CELEBRATION_TIME_S = 2

#settings
LEFT_CLICK = 1
RIGHT_CLICK = 3

#sprite images
SELECTOR_TOOL_IMAGE = pygame.transform.scale(pygame.image.load('resources/images/crosshair.png'), CELL_DIMENSIONS)