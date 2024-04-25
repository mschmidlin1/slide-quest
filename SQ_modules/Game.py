import pygame
from SQ_modules.GameBoard import GameBoard
from SQ_modules.DataTypes import Point, Size, Cell
from SQ_modules.LevelEditor import LevelEditor
from SQ_modules.LevelIO import LevelIO
from SQ_modules.GameEnums import Direction, GameDifficulty, CellType, sprite_positions, Screen
from SQ_modules.my_logging import set_logger, log
from SQ_modules.GameboardSpriteManager import GameboardSpriteManager
import logging
from SQ_modules.LevelBackground import LevelBackground
from SQ_modules.Sprites import Block, Goal, Ice, Player, SpriteLoader
from SQ_modules.ShortestPath import ShortestPath
from SQ_modules.GameAudio import GameAudio
from SQ_modules.NavigationManager import NavigationManager
from SQ_modules.configs import ( 
    WHITE,
    WINDOW_DIMENSIONS,
    CELL_DIMENSIONS,
    PLAYER_SPRITE_SHEET,
    IS_EDIT_ON_DEFAULT,
    Border_Size_Lookup,
    ENVIRONMENT_SPRITE_SHEET,
    COMPLETION_DELAY)

import copy
import time
set_logger()

class Game:
    """
    The controlling class for each "game" or "level" of slide quest.
    A game is born with each map and is destroyed once the player reaches the goal.
    """
    
    def __init__(self, screen: pygame.surface.Surface, gameboard: GameBoard):
        
        logging.info("New Game created.")
        self.game_audio = GameAudio()
        self.screen = screen
        self.isEditActive = IS_EDIT_ON_DEFAULT
        self.gameboard = gameboard
        self.border_size: Size = Border_Size_Lookup[self.gameboard.difficulty]
        self.game_complete_time = None
        self.solution_moves = ShortestPath(self.gameboard)
        self.shortest_path = copy.deepcopy(self.solution_moves)#save the original shortest path so the solution_moves can be updated as the player moves around
        self.least_moves = len(self.solution_moves)
        self.player_movable = True
        self.load_all_resources()
        self.gameboard_sprite_manager = GameboardSpriteManager(self.gameboard, self.screen)

        self.levelEditor = LevelEditor(self.gameboard, self.gameboard_sprite_manager, self.screen)
        self.level_background = LevelBackground(self.screen, "level text goes here", self.gameboard.difficulty)
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
                if event.key == Direction.LEFT.value:
                    direction = "LEFT"
                elif event.key == Direction.RIGHT.value:
                    direction = "RIGHT"
                elif event.key == Direction.UP.value:
                    direction = "UP"
                elif event.key == Direction.DOWN.value:
                    direction = "DOWN"
                
                if direction and not self.gameboard_sprite_manager.player_sprite.moving:
                    cell = self.gameboard.MovePlayer(Direction[direction])
                    self.gameboard_sprite_manager.Move(cell, direction)
                    self.num_moves += 1
                    self.game_audio.PlayRandomSlideSfx()

                if self.isEditActive:
                    self.solution_moves = ShortestPath(self.gameboard)

    
    def load_all_resources(self):
        SpriteLoader.load_sprite_sheet(ENVIRONMENT_SPRITE_SHEET, sprite_positions)

    
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
        current_time = pygame.time.get_ticks()

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
                if event.key == pygame.K_ESCAPE:
                    self.navigation_manager.navigate_to(Screen.OPTIONS)
        
        if self.isComplete() and not self.gameboard_sprite_manager.player_sprite.moving:
            if self.game_complete_time == None:
                self.player_movable = False
                self.game_complete_time = current_time + COMPLETION_DELAY
                self.game_audio.level_complete_sfx.play()
                self.gameboard_sprite_manager.player_sprite.current_type = 'celebrate'
                self.gameboard_sprite_manager.player_sprite.change_direction('DOWN')

            if self.game_complete_time and current_time - self.game_complete_time >= COMPLETION_DELAY:
                self.navigation_manager.navigate_to(Screen.LEVEL_COMPLETE)
                self.game_complete_time = None
    
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
