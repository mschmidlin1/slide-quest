from SQ_modules.Metas import SingletonMeta, SqScreenMeta
from SQ_modules.GameEnums import Screen
import pygame


class NavigationManager(metaclass=SingletonMeta):
    def __init__(self):
        


        self.current_screen: Screen = None
        self.game_active: bool = False


    def navigate_to(self, screen_type: Screen):
        """
        Navigate to the provided screen.
        """
        self.current_screen = screen_type


    