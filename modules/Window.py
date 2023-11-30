import sys
import pygame
from modules.LevelIO import LevelIO
from modules.TitleScreen import TitleScreen
from modules.LevelCompleteScreen import LevelCompleteScreen
from modules.Game import Game
from modules.configs import WINDOW_DIMENSIONS, WINDOW_TITLE, GAME_TYPE
from modules.my_logging import set_logger, log

set_logger()


class Window():
    """
    The manager of the pygame window and the main "screen" element. This class hands control of the screen to the various game screen the users sees. 
    """
    @log
    def __init__(self):
        self.new()
        self.title_screen: TitleScreen = TitleScreen(self.screen)
        self.current_game: Game = None
        self.level_complete_screen: LevelCompleteScreen = None
        self.level_manager = LevelIO()
    @log
    def new(self):
        """
        Creates a new pygame instance. Sets up the main screen 
        """
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
    @log
    def run(self):
        while True:
            events = pygame.event.get()
            self.update(events)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
    @log
    def draw(self):
        if self.title_screen is not None:
            self.title_screen.draw()
        elif self.level_complete_screen is not None:
            self.level_complete_screen.draw()
    @log
    def update(self, events):
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
                    self.level_complete_screen = LevelCompleteScreen(self.screen)
                    self.current_game = None
                    self.level_manager.next_level()
            else:        
                self.current_game.update(events)
