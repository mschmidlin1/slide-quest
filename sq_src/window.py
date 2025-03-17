import sys
import pygame
from sq_src.level_generation.level_io import LevelIO
from sq_src.screens.title_screen import TitleScreen
from sq_src.screens.level_complete_screen import LevelCompleteScreen
from sq_src.core.game import Game
from sq_src.configs import WINDOW_DIMENSIONS, WINDOW_TITLE, ICON, SPLASH_SCREEN_ON
from sq_src.singletons.banner_manager import BannerManager
from sq_src.singletons.my_logging import LoggingService
from sq_src.screens.splash_screen import SplashScreen
from sq_src.singletons.game_audio import GameAudio
from sq_src.data_structures.game_enums import Screen
from sq_src.screens.options_screen import OptionsScreen
from sq_src.singletons.navigation_manager import NavigationManager
from sq_src.singletons.level_manager import LevelManager
from sq_src.singletons.user_data import UserData
from sq_src.screens.welcome_screen import WelcomeScreen


class Window():
    """
    The manager of the pygame window and the main "screen" element. This class handles control of the screen to the various game screen the users sees. 
    """
    
    def __init__(self):
        self.new()
        self.user_data = UserData()
        self.title_screen: TitleScreen = None
        self.current_game: Game = None
        self.level_complete_screen: LevelCompleteScreen = None
        self.options_screen: OptionsScreen = None
        self.level_manager = LevelManager()
        self.game_audio = GameAudio()
        self.navigation_manager = NavigationManager()
        self.logging_service = LoggingService()
        self.banner_manager = BannerManager(self.screen)
        
        
    
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
        self.game_audio.splash_screen_sounds.play()
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

        self.game_audio.FadeInTitleScreenMusic()
        self.title_screen = TitleScreen(self.screen)
        self.welcome_screen = WelcomeScreen(self.screen)
        self.options_screen = OptionsScreen(self.screen)


        if self.user_data.get_user_name() == "": #if the user name is an empty string, launch the welcome screen.
            self.current_screen = self.welcome_screen
            self.current_screen_type = Screen.WELCOME
            self.navigation_manager.navigate_to(Screen.WELCOME)
        else:                                    #otherwise if there is a user name saved, go directly to title screen
            self.current_screen = self.title_screen
            self.current_screen_type = Screen.TITLE
            self.navigation_manager.navigate_to(Screen.TITLE)
        
        self.banner_manager.add_banner("Welcome!", 5)
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
        self.banner_manager.draw()
    

    def handle_navigation(self):
        """
        Handles the overall controls for which game screens are active.
        """
        #do nothing if the current screen has not been changed
        if self.current_screen_type == self.navigation_manager.current_screen:
            return
        self.logging_service.log_info(f"Navigating to {self.navigation_manager.current_screen}.")

        if self.navigation_manager.current_screen != Screen.LEVEL_COMPLETE:#don't play the navigation sound effect for level complete screen
            self.game_audio.button_click_sfx.play()
        if self.navigation_manager.current_screen == Screen.TITLE:
            if self.current_game is not None:
                self.level_manager.save_seed(self.current_game.shortest_path, False, 0, 0)
                self.current_game = None
                self.navigation_manager.game_active = False
            if not self.game_audio.is_music_on:
                self.game_audio.FadeInTitleScreenMusic()
            self.current_screen = self.title_screen
            self.current_screen_type = Screen.TITLE

        if self.navigation_manager.current_screen == Screen.OPTIONS:
            if not self.game_audio.is_music_on:
                self.game_audio.FadeInTitleScreenMusic()
            self.current_screen = self.options_screen
            self.current_screen_type = Screen.OPTIONS

        if self.navigation_manager.current_screen == Screen.LEVEL_COMPLETE:
            self.current_screen_type = Screen.LEVEL_COMPLETE
            if self.current_game.isComplete():
                self.level_manager.save_seed(self.current_game.shortest_path, True, self.current_game.total_time(), self.current_game.num_moves) #save the time and number of moves etc... This gets saved to the user data.
                stars = self.current_game.calculate_stars()
                self.level_complete_screen = LevelCompleteScreen(self.screen, self.current_game.num_moves, self.current_game.totalTime(), self.current_game.least_moves, stars)
                self.current_game = None
                self.navigation_manager.game_active = False

            self.current_screen = self.level_complete_screen
            

        if self.navigation_manager.current_screen == Screen.GAME:
            self.current_screen_type = Screen.GAME
            if self.current_game is None:
                self.level_manager.load_level(self.navigation_manager.curent_difficulty)
                self.current_game = Game(self.screen, self.level_manager.get_current_gameboard())
                self.navigation_manager.game_active = True
            if self.game_audio.is_music_on:
                self.game_audio.FadeOutTitleScreenMusic()
            self.current_screen = self.current_game
                

           


    def update(self, events: list[pygame.event.Event]):
        """
        Check for user input events and handle them.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.user_data.write()
                pygame.quit()
                sys.exit()
        #pass events to game audio
        self.game_audio.update(events)

        #pass events to which ever screen is current
        self.current_screen.update(events)

        self.banner_manager.update(events)

        #### Handle screen navigation #####
        self.handle_navigation()
