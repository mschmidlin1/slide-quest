import unittest
import sys
import os
import numpy as np
#necessary to import things from the SQ_modules folder
sys.path.append(os.getcwd())
from sq_src.data_structures.data_types import Point, Cell
from sq_src.data_structures.algorithms import ShortestPath, FindConnectedBlocks, FindConnectedGroups
from sq_src.data_structures.game_enums import GameDifficulty, CellType, Direction
from sq_src.core.game_board import GameBoard
cell_dtype = np.dtype(CellType)

class Test_FindConnectedBlocks(unittest.TestCase):
    def test_basic_test(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedBlocks(gameboard, start_cell=Cell(0, 7))
        self.assertEqual(4, len(blocks))

    def test_single(self):
        board = np.array([
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedBlocks(gameboard, start_cell=Cell(0, 0))
        self.assertEqual(1, len(blocks))
    
    def test_non_block(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        ices = FindConnectedBlocks(gameboard, start_cell=Cell(0, 1))
        self.assertEqual(99, len(ices))
        
    def test_diagonal(self):
        board = np.array([
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedBlocks(gameboard, start_cell=Cell(0, 0))
        self.assertEqual(1, len(blocks))
    
    def test_2x2(self):
        board = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedBlocks(gameboard, start_cell=Cell(0, 0))
        self.assertEqual(4, len(blocks))
        self.assertEqual(set([Cell(0, 0),Cell(1, 0),Cell(0, 1),Cell(1, 1)]), set(blocks))

    def test_vertical(self):
        board = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedBlocks(gameboard, start_cell=Cell(0, 0))
        self.assertEqual(4, len(blocks))
        self.assertEqual(set([Cell(0, 0),Cell(1, 0),Cell(0, 1),Cell(1, 1)]), set(blocks))

    def test_circle(self):
        board = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedBlocks(gameboard, start_cell=Cell(5,2))
        self.assertEqual(13, len(blocks))

    def test_two_different_points(self):
        board = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks1 = FindConnectedBlocks(gameboard, start_cell=Cell(5,2))
        blocks2 = FindConnectedBlocks(gameboard, start_cell=Cell(7,1))
        self.assertEqual(set(blocks1), set(blocks2))

class Test_FindConnectedGroups(unittest.TestCase):
    def test_basic(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedGroups(gameboard, CellType.BLOCK)
        self.assertEqual(2, len(blocks))

    def test_1(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedGroups(gameboard, CellType.BLOCK)
        self.assertEqual(1, len(blocks))
        self.assertEqual(4, len(blocks[0]))

    def test_0(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedGroups(gameboard, CellType.BLOCK)
        self.assertEqual(0, len(blocks))

    def test_ice(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedGroups(gameboard, CellType.ICE)
        self.assertEqual(1, len(blocks))
        self.assertEqual(99, len(blocks[0]))
    def test_diagonal(self):
        board = np.array([
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=5)
        gameboard = GameBoard(board, player_pos)
        blocks = FindConnectedGroups(gameboard, CellType.BLOCK)
        self.assertEqual(3, len(blocks))
        self.assertEqual(1, len(blocks[0]))
        self.assertIn(Cell(0, 0), blocks[0] + blocks[1] + blocks[2])
        self.assertIn(Cell(1, 1), blocks[0] + blocks[1] + blocks[2])
        self.assertIn(Cell(2, 2), blocks[0] + blocks[1] + blocks[2])


class Test_ShortestPath(unittest.TestCase):
    def test_1(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=0)
        gameboard = GameBoard(board, player_pos)
        moves = ShortestPath(gameboard)
        self.assertEqual(1, len(moves))
        self.assertEqual(Direction.RIGHT, moves[0])

    def test_2(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=8, row=9)
        gameboard = GameBoard(board, player_pos)
        moves = ShortestPath(gameboard)
        self.assertEqual(2, len(moves))
        self.assertEqual(Direction.UP, moves[0])

    def test_3(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=0, row=9)
        gameboard = GameBoard(board, player_pos)
        moves = ShortestPath(gameboard)
        self.assertEqual(3, len(moves))
        self.assertEqual(Direction.RIGHT, moves[0])
        self.assertEqual(Direction.UP, moves[1])
        self.assertEqual(Direction.RIGHT, moves[2])

    def test_4(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=0, row=0)
        gameboard = GameBoard(board, player_pos)
        moves = ShortestPath(gameboard)
        self.assertEqual(4, len(moves))
        self.assertEqual(Direction.DOWN, moves[0])
        self.assertEqual(Direction.RIGHT, moves[1])
        self.assertEqual(Direction.UP, moves[2])
        self.assertEqual(Direction.RIGHT, moves[3])

    def test_impossible(self):
        board = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.GOAL,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = Cell(col=0, row=0)
        gameboard = GameBoard(board, player_pos)
        moves = ShortestPath(gameboard)
        self.assertEqual(0, len(moves))



if __name__ == '__main__':
    unittest.main()