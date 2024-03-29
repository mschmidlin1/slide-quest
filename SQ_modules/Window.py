import sys
import pygame
from SQ_modules.LevelIO import LevelIO
from SQ_modules.TitleScreen import TitleScreen
from SQ_modules.LevelCompleteScreen import LevelCompleteScreen
from SQ_modules.Game import Game
from SQ_modules.configs import WINDOW_DIMENSIONS, WINDOW_TITLE, ICON
from SQ_modules.my_logging import set_logger, log
from SQ_modules.SplashScreen import SplashScreen

set_logger()


class Window():
    """
    The manager of the pygame window and the main "screen" element. This class handles control of the screen to the various game screen the users sees. 
    """
    
    def __init__(self):
        self.new()
        self.splash_screen_shown = False  # Add this to track if the splash screen has been shown
        self.title_screen: TitleScreen = None
        self.current_game: Game = None
        self.level_complete_screen: LevelCompleteScreen = None
        self.level_manager = LevelIO()
    
    def new(self):
        """
        Creates a new pygame instance. Sets up the main surface.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
        pygame.display.set_caption(WINDOW_TITLE)
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()

    
    def run_splash_screen(self):
        splash_screen = SplashScreen(self.screen)
        splash_screen.run()
        self.splash_screen_shown = True  # Mark splash screen as shown

    
    def run(self):
        """
        Main game loop.
        - updates events
        - draws sprites
        """
        if not self.splash_screen_shown:  # Show the splash screen before anything else
            self.run_splash_screen()    

        if not self.title_screen and self.splash_screen_shown:  # Initialize title_screen after splash
            self.title_screen = TitleScreen(self.screen)    

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
        if self.title_screen is not None:
            self.title_screen.draw()
        elif self.level_complete_screen is not None:
            self.level_complete_screen.draw()
        elif self.current_game is not None:
            self.current_game.draw()
    
    def update(self, events):
        """
        Check for user input events and handle them.
        """
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.title_screen != None: #if you're currently on the title screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_game = Game(self.screen, self.level_manager)
                        self.title_screen = None

            if self.current_game != None: #if you're currently playing the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.title_screen = TitleScreen(self.screen)
                    if event.key == pygame.K_r:
                        self.current_game = Game(self.screen, self.level_manager)

            if self.level_complete_screen != None: #if you're currently on the level complete screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_game = Game(self.screen, self.level_manager)
                        self.level_complete_screen = None

                    elif event.key == pygame.K_ESCAPE:
                        self.title_screen = TitleScreen(self.screen)
                        self.level_complete_screen = None

        #pulled isComplete() out of the event loop as it would not check completion unless an event was detected
        if self.current_game is not None:
            
            if self.current_game.isComplete():
                    self.level_complete_screen = LevelCompleteScreen(self.screen, self.current_game.num_moves, self.current_game.totalTime(), self.current_game.least_moves)
                    self.current_game = None
                    self.level_manager.next_level()
            else:        
                self.current_game.update(events)
