import pygame
from modules.GameBoard import GameBoard
from modules.MapConverter import update_map
from modules.Sprites import Block, Goal, Ice, Player
from modules.Point import Point
from modules.LevelEditor import LevelEditor
from modules.LevelIO import LevelIO
from modules.GameEnums import Direction, GameDifficulty, CellType
from modules.configs import (
    BEGINNER_DIMENSIONS, 
    ADVANCED_DIMENSIONS, 
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH, 
    CELL_HEIGHT,
    CELL_WIDTH,
    WINDOW_DIMENSIONS,)

class Game:
    """
    The controlling class for each "game" or "level" of slide quest.
    A game is born with each map and is destroyed once the player reaches the goal.
    """
    def __init__(self, screen: pygame.Surface, level_manager: LevelIO, debugging):
        
        print("New game")

        self.screen = screen
        # self.map_path(difficulty)

        # self.difficulty = difficulty
        self.debugging = debugging
        
        # if difficulty == GameDifficulty.BEGINNER:
        #     self.gameboard_dimensions = BEGINNER_DIMENSIONS
        # elif difficulty == GameDifficulty.ADVANCED:
        #     self.gameboard_dimensions = ADVANCED_DIMENSIONS
        # else:
        #     raise NotImplementedError("")
        
        # update_map(difficulty)

        gameboard, player_pos = level_manager.Read()

        self.gameboard = GameBoard(gameboard, player_pos)
        self.gameboard_sprite_group = pygame.sprite.LayeredUpdates()
        self.calculate_border()

        #implementation of GameBoard to initialize screen with all sprites from map csv
        for row, cells in enumerate(self.gameboard.gameboard):
            for col, cell in enumerate(cells):
                if cell == CellType.BLOCK:
                    self.gameboard_sprite_group.add(Block(Point(col, row), self.border_width, self.border_height))
                if cell == CellType.GOAL:
                    self.gameboard_sprite_group.add(Goal(Point(col, row), self.border_width, self.border_height))
                if cell == CellType.ICE:
                    self.gameboard_sprite_group.add(Ice(Point(col, row), self.border_width, self.border_height))

        self.player = Player(Point(1, 0), self.border_width, self.border_height)
        self.gameboard_sprite_group.add(self.player)

        self.levelEditor = LevelEditor(self, level_manager)

    # def update_map_text(self):
    #     with open('levels\\advanced\\map.txt', 'w') as file:
    #         for col in range(self.gameboard.gameboard_dims[1]): 
    #             for row in range(self.gameboard.gameboard_dims[0]):  
    #                 current_cell = (row, col)
    #                 for sprite in self.gameboard_sprite_group:
    #                     if current_cell == sprite.Get_Cell_Current_Position(sprite.rect.center) and not sprite.cellType == CellType.PLAYER:
    #                         file.write(str(sprite.cellType.value))
    #             file.write('\n')
    
    # def map_path(self, difficulty):
    #     if difficulty == GameDifficulty.BEGINNER:
    #         return 'levels\\beginner\\map.csv'
    #     elif difficulty == GameDifficulty.ADVANCED:
    #         return 'levels\\advanced\\map.csv'
        
    def debugging_toggle(self):
        self.debugging = not self.debugging

    def move_player(self, events: list[pygame.event.Event]):
        """
        Moves the player if instructed by the user in the events argument.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == Direction.LEFT.value and not self.player.moving:
                    self.player.move(self.gameboard.MovePlayer(Direction.LEFT))
                if event.key == Direction.RIGHT.value and not self.player.moving:
                    self.player.move(self.gameboard.MovePlayer(Direction.RIGHT))
                if event.key == Direction.UP.value and not self.player.moving:
                    self.player.move(self.gameboard.MovePlayer(Direction.UP))
                if event.key == Direction.DOWN.value and not self.player.moving:
                    self.player.move(self.gameboard.MovePlayer(Direction.DOWN))          

    def calculate_border(self):
        """
        This will store the width and height of the border for understanding the local gameboard positions
        """
        self.border_width = (WINDOW_DIMENSIONS[0] - (self.gameboard.gameboard.shape[0]*CELL_WIDTH))//2
        self.border_height = (WINDOW_DIMENSIONS[1] - (self.gameboard.gameboard.shape[1]*CELL_HEIGHT))//2

    def draw_grid(self, debug):
        """
        This is just temporary for showing the dimensions of the grid until we can start implementing sprites more regularly
        """
        if debug:
            for x in range(0, WINDOW_WIDTH, CELL_WIDTH):
                pygame.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
            for y in range(0, WINDOW_HEIGHT, CELL_HEIGHT):
                pygame.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y))

    def isComplete(self):
        """
        Checks whether the game has been completed.
        """
        if not self.player.moving:
            return self.gameboard.Find_Goal_Pos() == self.gameboard.GetPlayerPos()
    
    def update(self, events: list[pygame.event.Event]):
        """
        The Game.update() method takes a list of pygame events. From this the game will extract the necessary movement information for the player.
        """
        self.move_player(events)
        self.gameboard_sprite_group.update()
        self.gameboard_sprite_group.draw(self.screen)

        if(self.debugging):
            self.levelEditor.debugging(events)
            self.draw_grid(self.debugging)