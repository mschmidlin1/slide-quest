import asyncio
import sys
import pygame
from sq_src.level_generation.level_io import LevelIO
from sq_src.screens.title_screen import TitleScreen
from sq_src.screens.level_complete_screen import LevelCompleteScreen
from sq_src.core.game import Game
from sq_src.configs import (
    NAVY_BLUE,
    SPLASH_SCREEN_ON,
    TITLE_FONT,
    WHITE,
    WINDOW_DIMENSIONS,
    WINDOW_TITLE,
    ICON,
)
from sq_src.screens.tutorial import Tutorial
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
        pygame.display.set_caption("Slide Quest!" if sys.platform == "emscripten" else WINDOW_TITLE)
        pygame.display.set_icon(ICON)
        if sys.platform == "emscripten":
            self._style_browser_frame()
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

    def _style_browser_frame(self):
        """Navy page around the square, with the button cyan as a thin frame."""
        import platform
        platform.document.body.style.background = "#0B2A51"
        canvas = platform.window.canvas
        canvas.style.outline = "2px solid #43B8D6"
        canvas.style.outlineOffset = "0px"

    
    async def run_splash_screen(self):
        """
        Creates and instance of SplashScreen and runs it.
        """
        self.game_audio.splash_screen_sounds.play()
        splash_screen = SplashScreen(self.screen)
        return await splash_screen.run()

    def _shutdown(self):
        """Save progress and close the desktop window."""
        self.user_data.write()
        if sys.platform != "emscripten":
            pygame.quit()

    def _start_loaded_game(self):
        """Create the playable game from the level that just finished generating."""
        self.current_game = Game(self.screen, self.level_manager.get_current_gameboard())
        self.navigation_manager.game_active = True
        self.current_screen = self.current_game
        self.current_screen_type = Screen.GAME

    def _draw_loading(self):
        """Show a holding screen while a level is being generated."""
        self.screen.fill(NAVY_BLUE)
        if not hasattr(self, "_loading_text"):
            font = pygame.font.Font(TITLE_FONT, 80)
            self._loading_text = font.render("Generating level...", True, WHITE)
            self._loading_rect = self._loading_text.get_rect(
                center=(WINDOW_DIMENSIONS.width // 2, WINDOW_DIMENSIONS.height // 2)
            )
        self.screen.blit(self._loading_text, self._loading_rect)
    
    async def run(self):
        """
        Main game loop.
        - updates events
        - draws sprites
        """
        self._running = True
        if SPLASH_SCREEN_ON:
            if not await self.run_splash_screen():
                self._shutdown()
                return

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
        while self._running:
            events = pygame.event.get()
            self.update(events)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
            await asyncio.sleep(0)
        self._shutdown()
    
    def draw(self):
        """
        Draw window elements onto the screen.
        """
        if self.level_manager.is_loading or self.current_screen is None:
            self._draw_loading()
        else:
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
                # The level was left unfinished, so it earns no stars.
                # Game has no stars attribute; reading one used to kill the loop.
                self.level_manager.save_seed(self.current_game.shortest_path, False, 0, 0, 0)
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
                self.level_manager.save_seed(self.current_game.shortest_path, True, self.current_game.total_time(), self.current_game.num_moves, self.current_game.calculate_stars()) #save the time and number of moves etc... This gets saved to the user data.
                self.level_complete_screen = LevelCompleteScreen(self.screen, self.current_game.num_moves, self.current_game.totalTime(), self.current_game.least_moves, self.current_game.calculate_stars())
                self.current_game = None
                self.navigation_manager.game_active = False

            self.current_screen = self.level_complete_screen
            

        if self.navigation_manager.current_screen == Screen.GAME:
            self.current_screen_type = Screen.GAME
            if self.current_game is None:
                if not self.level_manager.is_loading:
                    self.level_manager.load_level(self.navigation_manager.curent_difficulty)
                if self.level_manager.is_loading:
                    self.current_screen = None
                else:
                    self._start_loaded_game()
            else:
                self.current_screen = self.current_game
            if self.game_audio.is_music_on:
                self.game_audio.FadeOutTitleScreenMusic()
                
        if self.navigation_manager.current_screen == Screen.TUTORIAL:
            self.current_screen_type = Screen.TUTORIAL
            if self.game_audio.is_music_on:
                self.game_audio.FadeOutTitleScreenMusic()
            self.current_screen = Tutorial(self.screen)


    def update(self, events: list[pygame.event.Event]):
        """
        Check for user input events and handle them.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
                return
        #pass events to game audio
        self.game_audio.update(events)

        if self.level_manager.is_loading:
            if self.level_manager.generation_step():
                self._start_loaded_game()
            self.banner_manager.update(events)
            return

        #pass events to which ever screen is current
        self.current_screen.update(events)

        self.banner_manager.update(events)

        #### Handle screen navigation #####
        self.handle_navigation()
