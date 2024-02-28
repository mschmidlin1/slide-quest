import pygame
from modules.GameBoard import GameBoard
from modules.Sprites import Block, Goal, Ice, Player
from modules.DataTypes import Point, Size
from modules.LevelEditor import LevelEditor
from modules.LevelIO import LevelIO
from modules.GameEnums import Direction, GameDifficulty, CellType
from modules.my_logging import set_logger, log
import logging
from modules.LevelBackground import LevelBackground
from modules.ShortestPath import ShortestPath
from modules.configs import ( 
    WHITE,
    WINDOW_DIMENSIONS,
    CELL_DIMENSIONS,
    IS_EDIT_ON_DEFAULT,
    Border_Size_Lookup)

import time
set_logger()

class Game:
    """
    The controlling class for each "game" or "level" of slide quest.
    A game is born with each map and is destroyed once the player reaches the goal.
    """
    @log
    def __init__(self, screen: pygame.surface.Surface, level_manager: LevelIO):
        
        logging.info("New Game created.")

        self.screen = screen
        self.isEditActive = IS_EDIT_ON_DEFAULT
        self.difficulty: GameDifficulty = level_manager.current_difficulty
        self.border_size: Size = Border_Size_Lookup[self.difficulty]
        gameboard_array, player_pos = level_manager.Read()
        self.gameboard = GameBoard(gameboard_array, player_pos)
        self.solution_moves = ShortestPath(self.gameboard)
        self.least_moves = len(self.solution_moves)
        self.gameboard_sprite_group = pygame.sprite.LayeredUpdates()
        for row, cells in enumerate(self.gameboard.gameboard):
            for col, cell in enumerate(cells):
                if cell == CellType.BLOCK:
                    self.gameboard_sprite_group.add(Block(Point(col, row), self.border_size))
                if cell == CellType.GOAL:
                    self.gameboard_sprite_group.add(Goal(Point(col, row), self.border_size))
                if cell == CellType.ICE:
                    self.gameboard_sprite_group.add(Ice(Point(col, row), self.border_size))

        self.player = Player(self.gameboard.player_pos, self.border_size)
        self.gameboard_sprite_group.add(self.player)
        self.levelEditor = LevelEditor(self.gameboard, self.gameboard_sprite_group, self.border_size, self.player, level_manager, self.screen)
        self.level_background = LevelBackground(self.screen, level_manager.current_level)
        self.num_moves = 0
        self.start_time = time.time()
    @log
    def move_player(self, events: list[pygame.event.Event]):
        """
        Moves the player if instructed by the user in the events argument.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == Direction.LEFT.value and not self.player.moving:
                    self.player.move(self.gameboard.MovePlayer(Direction.LEFT))
                    self.num_moves += 1
                if event.key == Direction.RIGHT.value and not self.player.moving:
                    self.player.move(self.gameboard.MovePlayer(Direction.RIGHT))
                    self.num_moves += 1
                if event.key == Direction.UP.value and not self.player.moving:
                    self.player.move(self.gameboard.MovePlayer(Direction.UP))
                    self.num_moves += 1
                if event.key == Direction.DOWN.value and not self.player.moving:
                    self.player.move(self.gameboard.MovePlayer(Direction.DOWN))
                    self.num_moves += 1
                if self.isEditActive:
                    self.solution_moves = ShortestPath(self.gameboard)       
    @log
    def isComplete(self):
        """
        Checks whether the game has been completed.
        """
        if not self.player.moving:
            return self.gameboard.Find_Goal_Pos() == self.gameboard.GetPlayerPos()
        else:
            return False
    @log
    def totalTime(self) -> str:
        """
        Gets the total time the level has taken so far to complete. 
        """
        total_time = time.time() - self.start_time
        minutes, seconds = divmod(total_time, 60)
        return f"{int(minutes):02}:{int(seconds):02}"
    @log
    def draw(self):
        """
        Draw the necessary game elements on the screen. Draws all child elements of the game (level_background and levelEditor).
        """
        #draw background first
        if(self.isEditActive):
            self.level_background.draw(self.totalTime(), self.solution_str())
        else:
            self.level_background.draw(self.totalTime(), "") # the solutions string won't be display if not in edit mode.
        
        #draw gameboard second
        self.gameboard_sprite_group.draw(self.screen)

        #draw level editor last
        if(self.isEditActive):
            self.levelEditor.draw()

    @log
    def update(self, events: list[pygame.event.Event]):
        """
        The Game.update() method takes a list of pygame events. From this the game will extract the necessary movement information for the player.

        This also passes the events to child elements such as levelEditor.
        """
        self.move_player(events)
        self.gameboard_sprite_group.update()

        if(self.isEditActive):
            self.levelEditor.update(events)
            

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.isEditActive = not self.isEditActive
            

    @log
    def solution_str(self) -> str:
        """
        Turns the self.solution_moves list into a human readable list for display.
        """

        return ",".join([self.move_str(dir) for dir in self.solution_moves])
    @log
    def move_str(self, move: Direction) -> str:
        """
        Turns the Direction.MOVE enum into just a string of "MOVE".
        """
        return str(move).split('.')[1]
