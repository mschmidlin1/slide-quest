import unittest
import pygame
from sq_src.configs import WINDOW_DIMENSIONS
from sq_src.core.gameboard_sprite_manager import SpriteType_To_CellType, CellType_To_SpriteType, GameboardSpriteManager
from sq_src.core.game_board import GameBoard
from sq_src.data_structures.game_enums import CellType, GameDifficulty
from sq_src.data_structures.data_types import Cell, Size
import numpy as np

from sq_src.sprites.background_spites import Block, Goal, Ice
from sq_src.sprites.player import Player
from sq_src.sprites.sprite_loader import SpriteLoader
cell_dtype = np.dtype(CellType)

def create_empty_gameboard(size: Size) -> GameBoard:
    """
    Creates a gameboard of ICE will the provided size. 

    Sets the GOAL position to [0,1] and the player position to [0,0].
    """
    gameboard = np.empty((size.height, size.width), dtype=cell_dtype)
    gameboard.fill(CellType.ICE)
    gameboard[0, 1] = CellType.GOAL
    return GameBoard(gameboard, Cell(0, 0))


SCREEN = pygame.display.set_mode(WINDOW_DIMENSIONS)

SpriteLoader.load_sprite_sheet()

class Test_CellType_To_Sprite(unittest.TestCase):
    def test_player(self):
        result = CellType_To_SpriteType(CellType.PLAYER)
        my_player_sprite = result(Cell(0, 0) , GameDifficulty.BEGINNER)
        self.assertEqual(result, Player)
        self.assertEqual(type(my_player_sprite), Player)

    def test_goal(self):
        result = CellType_To_SpriteType(CellType.GOAL)
        my_sprite = result(Cell(0, 0) , GameDifficulty.BEGINNER)
        self.assertEqual(result, Goal)
        self.assertEqual(type(my_sprite), Goal)

class Test_Sprite_To_CellType(unittest.TestCase):
    def test_player(self):
        result = SpriteType_To_CellType(Player)
        self.assertEqual(result, CellType.PLAYER)
    def test_block(self):
        block = Block(Cell(0, 0), GameDifficulty.BEGINNER)
        result = SpriteType_To_CellType(type(block))
        self.assertEqual(result, CellType.BLOCK)
    def test_instance(self):
        block = Block(Cell(0, 0), GameDifficulty.BEGINNER)
        with self.assertRaises(NotImplementedError):
            result = SpriteType_To_CellType(block)

class Test_Sprite_Manager(unittest.TestCase):
    def test_populate(self):
        my_gameboard = create_empty_gameboard(Size(10, 10))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)

        sprite_manager = GameboardSpriteManager(my_gameboard, SCREEN)
        self.assertEqual(100, len(sprite_manager.gameboard_sprite_group))


    def test_getsprite(self):
        my_gameboard = create_empty_gameboard(Size(10, 10))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)

        sprite_manager = GameboardSpriteManager(my_gameboard, SCREEN)
        self.assertEqual(Goal, type(sprite_manager.GetSprite(Cell(9, 9))))
        self.assertEqual(Ice, type(sprite_manager.GetSprite(Cell(5, 5))))


    def test_getcelltype(self):
        my_gameboard = create_empty_gameboard(Size(10, 10))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)

        sprite_manager = GameboardSpriteManager(my_gameboard, SCREEN)
        self.assertEqual(CellType.GOAL, sprite_manager.GetCellType(Cell(9, 9)))
        self.assertEqual(CellType.ICE, sprite_manager.GetCellType(Cell(5, 5)))

    def test_setsprite(self):
        my_gameboard = create_empty_gameboard(Size(10, 10))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)

        sprite_manager = GameboardSpriteManager(my_gameboard, SCREEN)
        sprite_manager.SetSprite(Cell(2, 2), CellType.BLOCK)

        self.assertEqual(CellType.BLOCK, sprite_manager.GetCellType(Cell(2, 2)))

        

if __name__ == '__main__':
    unittest.main()