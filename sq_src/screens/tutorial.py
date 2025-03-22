







import numpy as np
from sq_src.configs import BEGINNER_DIMENSIONS, CELEBRATION_TIME_S
from sq_src.core.game import Game
from sq_src.core.game_board import GameBoard
from sq_src.data_structures.data_types import Cell
from sq_src.data_structures.game_enums import CellType, Direction, Screen
import pygame

from sq_src.singletons.banner_manager import BannerManager
from sq_src.singletons.navigation_manager import NavigationManager
from sq_src.timer import Timer

cell_dtype = np.dtype(CellType)



class Tutorial:
    """A class that runs the game tutorial. It creates a special Game for the tutorial."""
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        ice_board = np.empty(BEGINNER_DIMENSIONS, dtype=cell_dtype)
        ice_board.fill(CellType.ICE)
        ice_board[5, 11] = CellType.GOAL

        gameboard = GameBoard(ice_board, Cell(0, 0), 0)
        self.game = Game(self.screen, gameboard)
        self.banner_manager = BannerManager()
        self.banner_manager.add_banner("Use arrow keys to Move!", 5, font_size = 23)
        self.navigation_manager = NavigationManager()
        self.set_blocks = False
        self.set_snow = False

    def update(self, events: list[pygame.event.Event]):
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                direction = None  # Placeholder for the direction
                if event.key in [Direction.RIGHT.value, pygame.K_d, Direction.DOWN.value, pygame.K_s] and not self.set_blocks:
                    self.game.gameboard.UpdateCell(Cell(row=0, col=5), CellType.BLOCK)
                    self.game.gameboard_sprite_manager.SetSprite(Cell(row=0, col=5), CellType.BLOCK)
                    self.game.gameboard.UpdateCell(Cell(row=3, col=0), CellType.BLOCK)
                    self.game.gameboard_sprite_manager.SetSprite(Cell(row=3, col=0), CellType.BLOCK)
                    self.banner_manager.add_banner("Ice sculptures block your path.", 5, font_size = 18)
                    self.set_blocks = True
                
                elif event.key in [Direction.RIGHT.value, pygame.K_d, Direction.DOWN.value, pygame.K_s] and not self.set_snow and self.game.gameboard.player_pos in [Cell(row=0, col=4), Cell(row=2, col=0)]:
                    self.game.gameboard.UpdateCell(Cell(row=2, col=4), CellType.GROUND)
                    self.game.gameboard_sprite_manager.SetSprite(Cell(row=2, col=4), CellType.GROUND)
                    self.banner_manager.add_banner("Snow lets you change direction.", 5, font_size = 18)
                    self.set_snow = True
        
        # self.game.update(events)

        if self.game.player_movable:
            self.game.move_player(events)

        self.game.gameboard_sprite_manager.update(events)


        self.game.level_background.update(self.game.totalTime(), "", False)
        if self.game.isComplete() and not self.game.gameboard_sprite_manager.player_sprite.moving:
            if self.game.celebration_timer == None:
                self.game.player_movable = False
                self.game.celebration_timer = Timer(CELEBRATION_TIME_S)
                self.game.celebration_timer.start()
                self.game.game_audio.level_complete_sfx.play()
                self.game.gameboard_sprite_manager.player_sprite.current_type = 'celebrate'
                self.game.gameboard_sprite_manager.player_sprite.change_direction('DOWN')

            if self.game.celebration_timer.time_is_up():
                self.navigation_manager.navigate_to(Screen.TITLE)
                self.game.celebration_timer = None
                self.banner_manager.add_banner("Tutorial Complete!", 5, font_size = 26)
    def draw(self):
        self.game.draw()