import pygame
from modules.GameBoard import GameBoard
from modules.Sprites import Block, Goal, Ice, Player
from modules.DataTypes import Point, Size
from modules.LevelEditor import LevelEditor
from modules.LevelIO import LevelIO
from modules.GameEnums import Direction, GameDifficulty, CellType
from modules.my_logging import set_logger, log
from modules.LevelBackground import LevelBackground
from modules.configs import ( 
    WHITE,
    WINDOW_DIMENSIONS,
    CELL_DIMENSIONS,
    EDIT_ON,
    Border_Size_Lookup)

import time


set_logger()

class Game:
    """
    The controlling class for each "game" or "level" of slide quest.
    A game is born with each map and is destroyed once the player reaches the goal.
    """
    @log
    def __init__(self, screen: pygame.Surface, level_manager: LevelIO):
        
        print("New game")

        self.screen = screen
        self.isEditActive = EDIT_ON
        self.difficulty: GameDifficulty = level_manager.current_difficulty
        self.border_size: Size = Border_Size_Lookup[self.difficulty]
        gameboard, player_pos = level_manager.Read()
        self.gameboard = GameBoard(gameboard, player_pos)
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
        self.levelEditor = LevelEditor(self, level_manager)
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
    @log
    def draw_grid(self):
        """
        This is just temporary for showing the dimensions of the grid until we can start implementing sprites more regularly
        """
        for x in range(0, WINDOW_DIMENSIONS.width, CELL_DIMENSIONS.width):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_DIMENSIONS.height))
        for y in range(0, WINDOW_DIMENSIONS.height, CELL_DIMENSIONS.height):
            pygame.draw.line(self.screen, WHITE, (0, y), (WINDOW_DIMENSIONS.width, y))
    @log
    def isComplete(self):
        """
        Checks whether the game has been completed.
        """
        if not self.player.moving:
            return self.gameboard.Find_Goal_Pos() == self.gameboard.GetPlayerPos()
    @log
    def totalTime(self) -> str:
        """
        Gets the total time the level has taken so far to complete. 
        """
        total_time = time.time() - self.start_time
        minutes, seconds = divmod(total_time, 60)
        return f"{int(minutes):02}:{int(seconds):02}"
    @log
    def update(self, events: list[pygame.event.Event]):
        """
        The Game.update() method takes a list of pygame events. From this the game will extract the necessary movement information for the player.
        """
        self.move_player(events)
        self.level_background.draw(self.totalTime())
        self.gameboard_sprite_group.update()
        self.gameboard_sprite_group.draw(self.screen)
        

        if(self.isEditActive):
            self.draw_grid()
            self.levelEditor.update(events)
            

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.isEditActive = not self.isEditActive
            

            