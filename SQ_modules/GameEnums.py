from enum import Enum
import pygame
import numpy as np


class Screen(Enum):
    """
    A class that represents the different buttons on the title screen.
    """
    TITLE = 0
    OPTIONS = 1
    GAME = 2
    LEVEL_COMPLETE = 3
    WELCOME = 4



class Direction(Enum):
    """
    An Enum class that handles user input conversion from pygame.
    """
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN

class GameDifficulty(Enum):
    """
    An Enum class that represents the overall game difficulty.
    """
    BEGINNER = 0
    INTERMEDIATE = 1
    HARD = 2
    EXPERT = 3

Game_Difficult_Str_Map = {
    "1": GameDifficulty.BEGINNER,
    "2": GameDifficulty.INTERMEDIATE,
    "3": GameDifficulty.HARD,
    "4": GameDifficulty.EXPERT
}

Game_Difficult_Str_Map_Reverse = {
    GameDifficulty.BEGINNER: "1",
    GameDifficulty.INTERMEDIATE: "2",
    GameDifficulty.HARD: "3",
    GameDifficulty.EXPERT: "4"
}

sprite_positions = {
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

class CellType(Enum):
    """
    An Enum class that represents the type of cell to fill the grid.
    """
    ICE = 0
    BLOCK = 1
    PLAYER = 2
    GOAL = 3
    PORTAL = 4
    POWER_UP = 5
    BORDER = 6
    GROUND = 7

# class GameMode(Enum):   -Mike changed to bool instead of Enum
#     """
#     This Enum will house the gametype between debugging or playing
#     """
#     EDIT_OFF = 0
#     EDIT_ON = 1

Str_to_CellType = {str(enum_member): enum_member for enum_member in CellType}

def Str_to_CellType_func(string):
    return Str_to_CellType[string]

Str_to_CellType_vector_func = np.vectorize(Str_to_CellType_func)