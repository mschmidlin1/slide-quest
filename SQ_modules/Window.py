import sys
import pygame
from SQ_modules.LevelIO import LevelIO
from SQ_modules.TitleScreen import TitleScreen
from SQ_modules.LevelCompleteScreen import LevelCompleteScreen
from SQ_modules.Game import Game
from SQ_modules.configs import WINDOW_DIMENSIONS, WINDOW_TITLE, ICON, SPLASH_SCREEN_ON
from SQ_modules.my_logging import set_logger, log
from SQ_modules.SplashScreen import SplashScreen
from SQ_modules.GameAudio import GameAudio
from SQ_modules.GameEnums import Screen
from SQ_modules.OptionsScreen import OptionsScreen
from SQ_modules.NavigationManager import NavigationManager

set_logger()


class Window():
    """
    The manager of the pygame window and the main "screen" element. This class handles control of the screen to the various game screen the users sees. 
    """
    
    def __init__(self):
        self.new()
        self.title_screen: TitleScreen = None
        self.current_game: Game = None
        self.level_complete_screen: LevelCompleteScreen = None
        self.options_screen: OptionsScreen = None
        self.level_manager = LevelIO()
        self.game_audio = GameAudio()
        self.navigation_manager = NavigationManager()
        self.game_audio.title_screen_music.play(fade_ms=5000, loops=-1)
    
    def new(self):
        """
        Creates a new pygame instance. Sets up the main surface.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
        pygame.display.set_caption(WINDOW_TITLE)
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

    
    def run_splash_screen(self):
        """
        Creates and instance of SplashScreen and runs it.
        """
        splash_screen = SplashScreen(self.screen)
        splash_screen.run()

    
    def run(self):
        """
        Main game loop.
        - updates events
        - draws sprites
        """
        if SPLASH_SCREEN_ON:
            self.run_splash_screen()    

        self.title_screen = TitleScreen(self.screen)    
        self.current_screen = self.title_screen
        self.current_screen_type = Screen.TITLE
        self.navigation_manager.navigate_to(Screen.TITLE)
        self.options_screen = OptionsScreen(self.screen)

        while True:
            events = pygame.event.get()
            self.update(events)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
    
    def draw(self):
        """
        Draw window elements onto the screen.
        """
        self.current_screen.draw()
        # if self.title_screen is not None:
        #     self.title_screen.draw()
        # elif self.level_complete_screen is not None:
        #     self.level_complete_screen.draw()
        # elif self.current_game is not None:
        #     self.current_game.draw()
        # elif self.options_screen is not None:
        #     self.options_screen.draw()
    

    def handle_navigation(self):
        """
        Handles the overall controls for which game screens are active.
        """
        #do nothing if the current screen has not been changed
        if self.current_screen_type == self.navigation_manager.current_screen:
            return


        if self.navigation_manager.current_screen == Screen.TITLE:
            self.current_screen = self.title_screen
            self.current_screen_type = Screen.TITLE

        if self.navigation_manager.current_screen == Screen.OPTIONS:
            self.current_screen = self.options_screen
            self.current_screen_type = Screen.OPTIONS

        if self.navigation_manager.current_screen == Screen.LEVEL_COMPLETE:
            self.current_screen_type = Screen.LEVEL_COMPLETE
            if self.current_game.isComplete():
                self.level_complete_screen = LevelCompleteScreen(self.screen, self.current_game.num_moves, self.current_game.totalTime(), self.current_game.least_moves)
                self.current_game = None
                self.navigation_manager.game_active = False
            self.current_screen = self.level_complete_screen
            

        if self.navigation_manager.current_screen == Screen.GAME:
            self.current_screen_type = Screen.GAME
            if self.current_game is None:
                self.current_game = Game(self.screen, self.level_manager, self.game_audio)
                self.navigation_manager.game_active = True
            self.current_screen = self.current_game
                



           


    def update(self, events: list[pygame.event.Event]):
        """
        Check for user input events and handle them.
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.current_screen.update(events)



        #### Handle Window events #####
        self.handle_navigation()
