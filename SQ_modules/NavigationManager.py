from SQ_modules.Metas import SingletonMeta, SqScreenMeta
from SQ_modules.GameEnums import Screen, GameDifficulty
import pygame


class NavigationManager(metaclass=SingletonMeta):
    """
    The navigation manager mostly keeps track of what screen the game is on.

    User the navigate_to() method to navigate to a new screen.

    The actual navigation happends in the window class. This class is a way to pass information back to the window class.
    """
    def __init__(self):
        


        self.current_screen: Screen = None
        self.game_active: bool = False
        self.curent_difficulty: GameDifficulty


    def navigate_to(self, screen_type: Screen):
        """
        Navigate to the provided screen.
        """
        self.current_screen = screen_type
    


    