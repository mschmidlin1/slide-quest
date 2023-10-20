import unittest
import sys
import os
#necessary to import things from the modules folder
sys.path.append(os.getcwd())
from modules.GameBoard import GameBoard
from modules.GameEnums import Direction, CellType
from modules.Point import Point

class Test__init__(unittest.TestCase):

    def test_gameboard_shape(self):
        for k in range(10):
            for l in range(10):
                my_gameboard = GameBoard((k, l))
                self.assertEqual(my_gameboard.gameboard.shape, (k, l))
                for i in range(k):
                    for j in range(l):
                        self.assertEqual(my_gameboard.gameboard[i, j], CellType.EMPTY)



class Test_UpdateCell(unittest.TestCase):
    def test_UpdatePlayerLoc_0_0(self):
        my_gameboard = GameBoard((10, 10))
        my_gameboard.UpdateCell(Point(0, 0), CellType.PLAYER)
        self.assertEqual(my_gameboard.gameboard[0, 0], CellType.PLAYER)
        self.assertEqual(my_gameboard.gameboard[0, 1], CellType.EMPTY)

    def test_UpdateBlockedLoc_1_1(self):
        my_gameboard = GameBoard((10, 10))
        my_gameboard.UpdateCell(Point(1, 1), CellType.BLOCKED)
        self.assertEqual(my_gameboard.gameboard[1, 1], CellType.BLOCKED)

    def test_UpdateGoalLoc_2_6(self):
        my_gameboard = GameBoard((10, 10))
        my_gameboard.UpdateCell(Point(2, 6), CellType.GOAL)
        self.assertEqual(my_gameboard.gameboard[2, 6], CellType.GOAL)
    
    def test_UpdateBorder(self):
        my_gameboard = GameBoard((10, 10))
        with self.assertRaises(ValueError):
            my_gameboard.UpdateCell(Point(2, 6), CellType.BORDER)
    
    def test_UpdateBorder(self):
        my_gameboard = GameBoard((10, 10))
        my_gameboard.UpdateCell(Point(2, 6), CellType.GOAL)
        with self.assertRaises(ValueError):
            my_gameboard.UpdateCell(Point(3, 6), CellType.GOAL)



if __name__ == '__main__':
    unittest.main()