import unittest
from SQ_modules.Converters import CellToPoint, PointToCell
from SQ_modules.DataTypes import Cell, Point
from SQ_modules.GameEnums import CellType, GameDifficulty
from SQ_modules.configs import CELL_DIMENSIONS, Border_Size_Lookup, WINDOW_DIMENSIONS
import sys
import os
import numpy as np
#necessary to import things from the SQ_modules folder
sys.path.append(os.getcwd())
from SQ_modules.GameBoard import GameBoard
from SQ_modules.GameEnums import Direction, CellType
from SQ_modules.DataTypes import Point, Cell
cell_dtype = np.dtype(CellType)





class Test_CellToPoint(unittest.TestCase):
    def test_outside_gameboard(self):
        difficulty = GameDifficulty.BEGINNER
        cell = Cell(100, 100)
        with self.assertRaises(ValueError):
            point = CellToPoint(cell, difficulty)

    def test_BEGINNER(self):
        difficulty = GameDifficulty.BEGINNER
        cell = Cell(row=0, col=0)
        point = CellToPoint(cell, difficulty)
        self.assertEqual(point, Point(288+(32//2), 288+(32//2)))

    def test_EXPERT(self):
        difficulty = GameDifficulty.EXPERT
        cell = Cell(row=0, col=0)
        point = CellToPoint(cell, difficulty)
        self.assertEqual(point, Point(64+(32//2), 64+(32//2)))
    def test_EXPERT_bottom_right(self):
        difficulty = GameDifficulty.EXPERT
        cell = Cell(row=25, col=25)
        point = CellToPoint(cell, difficulty)
        self.assertEqual(point, Point(64+(25*32)+(32//2), 64+(25*32)+(32//2)))
                         
    def test_outside_right(self):
        difficulty = GameDifficulty.EXPERT
        cell = Cell(row=26, col=26)
        with self.assertRaises(ValueError):
            point = CellToPoint(cell, difficulty)
    def test_negative(self):
        difficulty = GameDifficulty.EXPERT
        cell = Cell(row=-1, col=-1)
        with self.assertRaises(ValueError):
            point = CellToPoint(cell, difficulty)

class Test_PointToCell(unittest.TestCase):
    def test_off_gameboard(self):
        difficulty = GameDifficulty.BEGINNER
        point = Point(0, 0)
        cell = PointToCell(point, difficulty)
        self.assertIsNone(cell)
    def test_bottom_right_expert(self):
        point = Point(64+(25*32)+(32//2)+4, 64+(25*32)+(32//2)-3)
        difficulty = GameDifficulty.EXPERT
        cell = PointToCell(point, difficulty)
        self.assertEqual(cell, Cell(25, 25))
    def test_bottom_right_beginner(self):
        point = Point(64+(25*32)+(32//2)+4, 64+(25*32)+(32//2)-3)
        difficulty = GameDifficulty.BEGINNER
        cell = PointToCell(point, difficulty)
        self.assertIsNone(cell)
    def test_BEGINNER(self):
        point = Point(288, 288)
        difficulty = GameDifficulty.BEGINNER
        cell = PointToCell(point, difficulty)
        self.assertEqual(cell, Cell(0, 0))
    def test_EXPERT(self):
        point = Point(64, 64)
        difficulty = GameDifficulty.EXPERT
        cell = PointToCell(point, difficulty)
        self.assertEqual(cell, Cell(0, 0))