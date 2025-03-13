import pygame
from sq_src.core.game_board import GameBoard
from sq_src.data_structures.data_types import Point, Size, Cell
from sq_src.level_generation.level_editor import LevelEditor
from sq_src.level_generation.level_io import LevelIO
from sq_src.data_structures.game_enums import Direction, GameDifficulty, CellType, Screen
from sq_src.singletons.my_logging import LoggingService
from sq_src.core.gameboard_sprite_manager import GameboardSpriteManager
from sq_src.core.level_background import LevelBackground
from sq_src.data_structures.algorithms import ShortestPath
from sq_src.singletons.game_audio import GameAudio
from sq_src.singletons.navigation_manager import NavigationManager
from sq_src.sprites.sprite_loader import SpriteLoader
from sq_src.timer import Timer
from sq_src.configs import ( 
    WHITE,
    WINDOW_DIMENSIONS,
    CELL_DIMENSIONS,
    PLAYER_SPRITE_SHEET,
    IS_EDIT_ON_DEFAULT,
    Border_Size_Lookup,
    ENVIRONMENT_SPRITE_SHEET,
    CELEBRATION_TIME_S, 
    SPRITE_POSITIONS)

import copy
import time

class Game:
    """
    The controlling class for each "game" or "level" of slide quest.
    A game is born with each map and is destroyed once the player reaches the goal.
    """
    
    def __init__(self, screen: pygame.surface.Surface, gameboard: GameBoard):
        self.logging_service = LoggingService()
        self.logging_service.log_info("New Game created.")
        self.game_audio = GameAudio()
        self.screen = screen
        self.isEditActive = IS_EDIT_ON_DEFAULT
        self.gameboard = gameboard
        self.border_size: Size = Border_Size_Lookup[self.gameboard.difficulty]
        self.celebration_timer = None
        self.solution_moves = ShortestPath(self.gameboard)
        self.shortest_path = copy.deepcopy(self.solution_moves)#save the original shortest path so the solution_moves can be updated as the player moves around
        self.least_moves = len(self.solution_moves)
        self.player_movable = True
        self.load_all_resources()
        self.gameboard_sprite_manager = GameboardSpriteManager(self.gameboard, self.screen)

        self.levelEditor = LevelEditor(self.gameboard, self.gameboard_sprite_manager, self.screen)
        self.level_background = LevelBackground(self.screen, f"Map seed: {self.gameboard.seed}", self.gameboard.difficulty)
        self.level_background.fill_background()
        self.num_moves = 0
        self.navigation_manager = NavigationManager()

        self.start_time = time.time()

    def move_player(self, events: list[pygame.event.Event]):
        """
        Moves the player if instructed by the user in the events argument.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                direction = None  # Placeholder for the direction
                if event.key == Direction.LEFT.value or event.key == pygame.K_a:
                    direction = "LEFT"
                elif event.key == Direction.RIGHT.value or event.key == pygame.K_d:
                    direction = "RIGHT"
                elif event.key == Direction.UP.value or event.key == pygame.K_w:
                    direction = "UP"
                elif event.key == Direction.DOWN.value or event.key == pygame.K_s:
                    direction = "DOWN"
                
                if direction and not self.gameboard_sprite_manager.player_sprite.moving:
                    cell = self.gameboard.MovePlayer(Direction[direction])
                    self.gameboard_sprite_manager.MovePlayer(cell, direction)
                    self.num_moves += 1
                    self.game_audio.PlayRandomSlideSfx()

                if self.isEditActive:
                    self.solution_moves = ShortestPath(self.gameboard)

    
    def load_all_resources(self):
        SpriteLoader.load_sprite_sheet()

    
    def isComplete(self):
        """
        Checks whether the game has been completed.
        """
        if not self.gameboard_sprite_manager.player_sprite.moving:
            return self.gameboard.Find_Goal_Pos() == self.gameboard.GetPlayerPos()
        else:
            return False
    
    def total_time(self) -> float:
        """
        Gets the total time the level has taken so far to complete.
        """
        return time.time() - self.start_time
    
    def totalTime(self) -> str:
        """
        Gets the total time the level has taken so far to complete. 
        """
        total_time = time.time() - self.start_time
        minutes, seconds = divmod(total_time, 60)
        return f"{int(minutes):02}:{int(seconds):02}"
    
    
    def draw(self):
        """
        Draw the necessary game elements on the screen. Draws all child elements of the game (level_background and levelEditor).
        """
        #draw background first
        self.level_background.background_sprites.draw(self.screen)

        if(self.isEditActive):
            self.level_background.draw(self.totalTime(), self.solution_str())
        else:
            self.level_background.draw(self.totalTime(), "") # the solutions string won't be display if not in edit mode.
        
        #draw sprite second
        self.gameboard_sprite_manager.draw()

        #draw level editor last
        if(self.isEditActive):
            self.levelEditor.draw()
        else:
            self.level_background.bottom_border_sprites.draw(self.screen)


    
    def update(self, events: list[pygame.event.Event]):
        """
        The Game.update() method takes a list of pygame events. From this the game will extract the necessary movement information for the player.

        This also passes the events to child elements such as levelEditor.
        """

        if self.player_movable:
            self.move_player(events)

        self.gameboard_sprite_manager.update(events)

        if(self.isEditActive):
            self.levelEditor.update(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if self.levelEditor.drag_type is None:#only let the level editor be turned off if a click and drag operation is not happening
                        self.isEditActive = not self.isEditActive
                        if self.isEditActive:
                            self.gameboard_sprite_manager.toggle_editor_on()
                        else:
                            self.gameboard_sprite_manager.toggle_editor_off()
                        if not self.isEditActive:
                            self.gameboard_sprite_manager.ClearAndPopulateGameSprites()
                if event.key == pygame.K_ESCAPE:
                    self.navigation_manager.navigate_to(Screen.OPTIONS)
        
        if self.isComplete() and not self.gameboard_sprite_manager.player_sprite.moving:
            if self.celebration_timer == None:
                self.player_movable = False
                self.celebration_timer = Timer(CELEBRATION_TIME_S)
                self.celebration_timer.start()
                self.game_audio.level_complete_sfx.play()
                self.gameboard_sprite_manager.player_sprite.current_type = 'celebrate'
                self.gameboard_sprite_manager.player_sprite.change_direction('DOWN')

            if self.celebration_timer.time_is_up():
                self.navigation_manager.navigate_to(Screen.LEVEL_COMPLETE)
                self.celebration_timer = None
    
    def solution_str(self) -> str:
        """
        Turns the self.solution_moves list into a human readable list for display.
        """

        return ",".join([self.move_str(dir) for dir in self.solution_moves])
    
    def move_str(self, move: Direction) -> str:
        """
        Turns the Direction.MOVE enum into just a string of "MOVE".
        """
        return str(move).split('.')[1]
