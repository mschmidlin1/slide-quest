import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.GameEnums import GameDifficulty

#game settings
WINDOW_TITLE = "Slide Quest"

TITLE_FONT = "resources/fonts/Chunk Five Print.otf"

#window information

#must be set to a multiple of 64
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 960
WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)

BEGINNER_DIMENSIONS = (12, 12)
INTERMEDIATE_DIMENSIONS = (18, 18)
HARD_DIMENSIONS = (22, 22)
ADVANCED_DIMENSIONS = (26, 26)

#difficulty
CURRENT_DIFFICULTY = GameDifficulty.ADVANCED

#cell information
CELLSIZE = 32
CELL_WIDTH, CELL_HEIGHT = 32, 32
CELL_DIMENSIONS = (CELL_WIDTH,  CELL_HEIGHT)

#define colors
TITLE_SCREEN_COLOR = (37, 150, 190)
TITLE_SCREEN_TEXT_COLOR = (226, 135, 67)
BGCOLOR = (140, 140, 140)
WHITE = (255, 255, 255)
PLAYER_COLOR = (123, 5, 75)
WALL_COLOR = (2, 100, 75)
GOAL_COLOR = (22, 140, 189)
ICE_COLOR = (173, 216, 230)

#other constants
PLAYER_SPEED = .2