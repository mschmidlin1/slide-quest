from modules.GameBoard import GameBoard
import pygame
from modules.MapConverter import update_map
from modules.Sprites import Block, Goal, Ice, Player 
import sys
from modules.Point import Point
from modules.GameEnums import Direction, GameDifficulty, CellType
from modules.configs import (
    WINDOW_TITLE, 
    ADVANCED_DIMENSIONS, 
    BGCOLOR,
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
    def __init__(self, difficulty: GameDifficulty, screen):
        self.screen = screen
        self.difficulty = difficulty
        if difficulty==GameDifficulty.ADVANCED:
            self.gameboard_dimensions = ADVANCED_DIMENSIONS
        else:
            raise NotImplementedError("")
        
        self.gameboard = GameBoard(self.gameboard_dimensions)
        self.gameboard_sprite_group = pygame.sprite.LayeredUpdates()
        self.calculate_border()
        #Update map.csv
        # update_map()

        self.gameboard.ReadBoard('levels\\beginner\\map.csv')

        #implementation of GameBoard to initialize screen with all sprites from map csv
        for row, cells in enumerate(self.gameboard.gameboard):
            for col, cell in enumerate(cells):
                if cell == CellType.BLOCK:
                    self.gameboard_sprite_group.add(Block(Point(col, row), self.border_width, self.border_height))
                if cell == CellType.GOAL:
                    self.gameboard_sprite_group.add(Goal(Point(col, row), self.border_width, self.border_height))
                if cell == CellType.ICE:
                    self.gameboard_sprite_group.add(Ice(Point(col, row), self.border_width, self.border_height))
        self.gameboard.SetPlayerPos(Point(1, 1))
        self.player = Player(Point(1, 1), self.border_width, self.border_height)
        self.gameboard_sprite_group.add(self.player)

    def move_player(self, events: list[pygame.event.Event]):
        """
        Moves the player if instructed by the user in the events argument.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == Direction.LEFT.value:
                    self.player.move(self.gameboard.MovePlayer(Direction.LEFT))
                if event.key == Direction.RIGHT.value:
                    self.player.move(self.gameboard.MovePlayer(Direction.RIGHT))
                if event.key == Direction.UP.value:
                    self.player.move(self.gameboard.MovePlayer(Direction.UP))
                if event.key == Direction.DOWN.value:
                    self.player.move(self.gameboard.MovePlayer(Direction.DOWN))

    def calculate_border(self):
        """
        """
        self.border_width = (WINDOW_DIMENSIONS[0] - (self.gameboard_dimensions[0]*CELL_WIDTH))//2
        self.border_height = (WINDOW_DIMENSIONS[1] - (self.gameboard_dimensions[1]*CELL_HEIGHT))//2

    # def draw_grid(self):
    #     """
    #     This is just temporary for showing the dimensions of the grid until we can start implementing sprites more regularly
    #     """

    #     for x in range(0, WINDOW_WIDTH, CELL_WIDTH):
    #         pygame.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    #     for y in range(0, WINDOW_HEIGHT, CELL_HEIGHT):
    #         pygame.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y))

    # def draw(self):
    #     """
    #     Draw the sprite groups to the screen as well as handle the screen updating (pygame.display.flip())
    #     """

    #     self.screen.fill(BGCOLOR)
    #     self.all_sprites.draw(self.screen)
    #     self.draw_grid()
    #     #this is for updating the entire sceen instead of pygame.display.update which only updates a portion
    #     pygame.display.flip()

    def isComplete(self):
        """
        Checks whether the game has been completed.
        """
        return self.gameboard.Find_Goal_Pos() == self.gameboard.player_pos
    def update(self, events: list[pygame.event.Event]):
        """
        The Game.update() method takes a list of pygame events. From this the game will extract the necessary movement information for the player.
        """
        self.move_player(events)
        self.gameboard_sprite_group.update()
        self.gameboard_sprite_group.draw(self.screen)