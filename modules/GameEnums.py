from enum import Enum
import pygame

class Direction(Enum):
    """
    An Enum class that handles user input conversion from pygame.
    """
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN

class GameLevel(Enum):
    """
    An Enum class that represents the overall game difficulty.
    """
    BEGINNER = 0
    INTERMEDIATE = 1
    HARD = 2
    ADVANCED = 3

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