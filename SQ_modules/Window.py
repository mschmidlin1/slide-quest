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
from SQ_modules.GameEnums import TitleScreenButton
from SQ_modules.OptionsScreen import OptionsScreen

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
        elif self.options_screen is not None:
            self.options_screen.draw()
    

    def handle_window_navigation(self, events: list[pygame.event.Event]):
        """
        Handles the overall controls for which game screens are active.
        """
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.title_screen != None: #if you're currently on the title screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_game = Game(self.screen, self.level_manager, self.game_audio)
                        self.title_screen = None
                        self.game_audio.title_screen_music.stop()
                    
                    
                elif self.title_screen.click_type is not None:
                    if self.title_screen.click_type == TitleScreenButton.OPTIONS:
                        self.options_screen = OptionsScreen(self.screen)
                        self.title_screen = None

            if self.current_game != None: #if you're currently playing the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.title_screen = TitleScreen(self.screen)
                        self.game_audio.title_screen_music.play(fade_ms=5000, loops=-1)
                    if event.key == pygame.K_r:
                        self.current_game = Game(self.screen, self.level_manager, self.game_audio)

            if self.level_complete_screen != None: #if you're currently on the level complete screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_game = Game(self.screen, self.level_manager, self.game_audio)
                        self.level_complete_screen = None


                    elif event.key == pygame.K_ESCAPE:
                        self.title_screen = TitleScreen(self.screen)
                        self.game_audio.title_screen_music.play(fade_ms=5000, loops=-1)
                        self.level_complete_screen = None
            
            if self.options_screen is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.title_screen = TitleScreen(self.screen)
                        self.options_screen = None


    def update(self, events: list[pygame.event.Event]):
        """
        Check for user input events and handle them.
        """



        #pulled isComplete() out of the event loop as it would not check completion unless an event was detected
        if self.current_game is not None:
            
            if self.current_game.isComplete():
                    self.game_audio.level_complete_sfx.play()
                    self.level_complete_screen = LevelCompleteScreen(self.screen, self.current_game.num_moves, self.current_game.totalTime(), self.current_game.least_moves)
                    self.current_game = None
                    self.level_manager.next_level()
            else:        
                self.current_game.update(events)
        
        if self.title_screen is not None:
            self.title_screen.update(events)

        if self.options_screen is not None:
            self.options_screen.update(events)



        #### Handle Window events #####
        self.handle_window_navigation(events)
