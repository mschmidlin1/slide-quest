from enum import Enum
import pygame
import numpy as np


class Screen(Enum):
    """
    A Enum class that represents the main screens of the SQ game.
    A main screen is any screen that draws on the entire window.
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
    TEST = 4

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