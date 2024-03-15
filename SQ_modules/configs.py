import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SQ_modules.GameEnums import GameDifficulty
from SQ_modules.DataTypes import Size
import pygame

#logging settings
FILE_LOG_LEVEL = "DEBUG"
STDOUT_LOG_LEVEL = "INFO"


#game settings
WINDOW_TITLE = "Slide Quest"
ICON = pygame.image.load('resources/images/Icy-Q-nobackground64x64.png')
TITLE_FONT = "resources/fonts/m5x7.otf"
PLAYER_SPRITE_SHEET = 'resources/sprites/player/adventurer-grey-scarf-Sheet.png'
PLAYERSHADOW_SPRITE_SHEET = 'resources/sprites/player/player-shadow.png'

#window information


WINDOW_DIMENSIONS = Size(width=960, height=960) #must be set to a multiple of 64
CELL_DIMENSIONS = Size(width=32,  height=32)
BEGINNER_DIMENSIONS = Size(width=12, height=12)
INTERMEDIATE_DIMENSIONS = Size(width=18, height=18)
HARD_DIMENSIONS = Size(width=22, height=22)
EXPERT_DIMENSIONS = Size(width=26, height=26)

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

Border_Size_Lookup = {
        GameDifficulty.BEGINNER: BEGINNER_BORDER,
        GameDifficulty.INTERMEDIATE: INTERMEDIATE_BORDER,
        GameDifficulty.HARD: HARD_BORDER,
        GameDifficulty.EXPERT: EXPERT_BORDER
}

Board_Size_Lookup = {
        GameDifficulty.BEGINNER: BEGINNER_DIMENSIONS,
        GameDifficulty.INTERMEDIATE: INTERMEDIATE_DIMENSIONS,
        GameDifficulty.HARD: HARD_DIMENSIONS,
        GameDifficulty.EXPERT: EXPERT_DIMENSIONS
}

#Defaul to edit on or edit off
IS_EDIT_ON_DEFAULT = False

#cell information


#define colors
TITLE_SCREEN_COLOR = (37, 150, 190)
TITLE_SCREEN_TEXT_COLOR = (255, 255, 255)
BGCOLOR = (140, 140, 140)
WHITE = (255, 255, 255)
PLAYER_COLOR = (123, 5, 75)
WALL_COLOR = (2, 100, 75)
GOAL_COLOR = (255, 255, 0)
ICE_COLOR = (173, 216, 230)
PALLET_HIGHLIGHT_COLOR = (230, 237, 28)

#other constants
PLAYER_SPEED = .3

#settings
LEFT_CLICK = 1
RIGHT_CLICK = 3


#sprite images
SELECTOR_TOOL_IMAGE = pygame.transform.scale(pygame.image.load('resources/images/crosshair.png'), CELL_DIMENSIONS)