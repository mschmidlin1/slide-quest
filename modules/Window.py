import sys
import pygame
import time
from modules.GameEnums import GameMode, CellType
from modules.TitleScreen import TitleScreen
from modules.LevelCompleteScreen import LevelCompleteScreen
from modules.Sprites import Block, Ice
from modules.Game import Game
from modules.configs import CURRENT_DIFFICULTY, WINDOW_DIMENSIONS, WINDOW_TITLE, GAME_TYPE
from modules.my_logging import set_logger, log
from modules.MapConverter import update_map

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
            self.handle_events(events)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
    @log
    def draw(self):
        if self.title_screen is not None:
            self.title_screen.draw()
        # elif self.current_game is not None:
        #     self.current_game.draw(self.screen)
        elif self.level_complete_screen is not None:
            self.level_complete_screen.draw()
    @log
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.title_screen != None: #if you're currently on the title screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_game = Game(CURRENT_DIFFICULTY, self.screen)
                        self.title_screen = None

            if self.current_game != None: #if you're currently playing the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.title_screen = TitleScreen(self.screen)
                        self.current_game = None
                if event.type == pygame.MOUSEBUTTONDOWN and GAME_TYPE == GameMode.DEBUG_MODE:
                    click_pos = pygame.mouse.get_pos()
                    clicked_cells = [clicked_cell for clicked_cell in self.current_game.gameboard_sprite_group if clicked_cell.rect.collidepoint(click_pos)]
                    if clicked_cells:
                        top_cell = clicked_cells[-1]
                        curr_pos = top_cell.Get_Cell_Current_Position(top_cell.rect.center)
                        if event.button == 1: #LEFT CLICK
                            print(f"Cell clicked at center: {curr_pos}")
                            print(top_cell.cellType)
                            if top_cell.cellType == CellType.ICE:
                                self.current_game.gameboard_sprite_group.remove(top_cell)
                                self.current_game.gameboard_sprite_group.add(Block(curr_pos, self.current_game.border_width, self.current_game.border_height))
                                self.current_game.update_map_text()
                                update_map(CURRENT_DIFFICULTY)
                                self.current_game.gameboard.ReadBoard('levels\\advanced\\map.csv')
                        if event.button == 3: #RIGHT CLICK
                            if top_cell.cellType == CellType.BLOCK:
                                self.current_game.gameboard_sprite_group.remove(top_cell)
                                self.current_game.gameboard_sprite_group.add(Ice(curr_pos, self.current_game.border_width, self.current_game.border_height))
                                self.current_game.update_map_text()
                                update_map(CURRENT_DIFFICULTY)
                                self.current_game.gameboard.ReadBoard('levels\\advanced\\map.csv')

            if self.level_complete_screen != None: #if you're currently on the level complete screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_game = Game(CURRENT_DIFFICULTY, self.screen)
                        self.level_complete_screen = None

                    elif event.key == pygame.K_ESCAPE:
                        self.title_screen = TitleScreen(self.screen)
                        self.level_complete_screen = None

        #pulled isComplete() out of the event loop as it would not check completion unless an event was detected
        if self.current_game is not None:
            if self.current_game.isComplete():
                    self.level_complete_screen = LevelCompleteScreen(self.screen)
                    self.current_game = None
            else:        
                self.current_game.update(events)



