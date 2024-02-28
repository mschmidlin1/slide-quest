import unittest
import sys
import os
import numpy as np
#necessary to import things from the modules folder
sys.path.append(os.getcwd())
from modules.GameBoard import GameBoard
from modules.GameEnums import Direction, CellType
from modules.DataTypes import Point, Cell
cell_dtype = np.dtype(CellType)

class Test_UpdateCell(unittest.TestCase):
    def test_UpdatePlayerLoc_0_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        with self.assertRaises(ValueError):
            my_gameboard.UpdateCell(Cell(0, 0), CellType.PLAYER)
        self.assertEqual(my_gameboard.gameboard[1, 1], CellType.ICE)

    def test_UpdateBlock_onplayer(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.SetPlayerPos(Cell(0, 0))
        with self.assertRaises(ValueError):
            my_gameboard.UpdateCell(Cell(0, 0), CellType.BLOCK)
    
    def test_UpdateBlockedLoc_1_1(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.UpdateCell(Cell(1, 1), CellType.BLOCK)
        self.assertEqual(my_gameboard.gameboard[1, 1], CellType.BLOCK)

    def test_UpdateGoalLoc_2_6(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        with self.assertRaises(ValueError):
            my_gameboard.UpdateCell(Cell(6, 2), CellType.GOAL)
        self.assertEqual(my_gameboard.gameboard[0, 1], CellType.GOAL)
    
    def test_UpdateBorder(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        with self.assertRaises(ValueError):
            my_gameboard.UpdateCell(Cell(6, 2), CellType.BORDER)

class Test_playerPresent(unittest.TestCase):
    def test_playerPresent_withPlayer(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.SetPlayerPos(Cell(0, 0))
        self.assertTrue(my_gameboard.playerPresent())

    def test_playerPresent_withoutPlayer(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.player_pos = None
        self.assertFalse(my_gameboard.playerPresent())

class Test_blockerPresent(unittest.TestCase):
    def test_blockerPresent_withBlock(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.UpdateCell(Cell(5, 0), CellType.BLOCK)
        self.assertTrue(my_gameboard.blockerPresent())

    def test_blockerPresent_withoutBlock(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        self.assertFalse(my_gameboard.blockerPresent())

    def test_blockerPresent_with2Block(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.UpdateCell(Cell(0, 5), CellType.BLOCK)
        my_gameboard.UpdateCell(Cell(1, 1), CellType.BLOCK)
        self.assertTrue(my_gameboard.blockerPresent())


class Test_goalPresent(unittest.TestCase):
    def test_goalPresent_withGoal(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        self.assertTrue(my_gameboard.goalPresent())

    def test_goalPresent_withoutGoal(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard[0, 1] = CellType.ICE
        self.assertFalse(my_gameboard.goalPresent())

class Test_SetPlayerPos(unittest.TestCase):
    def test_SetPlayerPos_None(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.player_pos = None
        self.assertEqual(my_gameboard.player_pos, None)
    def test_SetPlayerPos_0_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        self.assertEqual(my_gameboard.player_pos, Cell(0, 0))

    def test_SetPlayerPos_on_block(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(1, 1))
        my_gameboard.UpdateCell(Cell(0, 0), CellType.BLOCK)
        with self.assertRaises(ValueError):
            my_gameboard.SetPlayerPos(Cell(0, 0))

class Test_GetPlayerPos(unittest.TestCase):
    def test_GetPlayerPos_present(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        self.assertEqual(my_gameboard.GetPlayerPos(), Cell(0, 0))
    
    def test_GetPlayerPos_NOTpresent(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.player_pos = None
        with self.assertRaises(RuntimeError):
            my_gameboard.GetPlayerPos()

class Test_Find_Goal_Pos(unittest.TestCase):
    def test_Find_Goal_Pos_0_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 0] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(1, 1))
        pos = my_gameboard.Find_Goal_Pos()
        self.assertEqual(pos, Cell(0, 0))

    def test_Find_Goal_Pos_1_3(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[3, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        pos = my_gameboard.Find_Goal_Pos()
        self.assertEqual(pos, Cell(3, 1))

    def test_Find_Goal_Pos_withoutGoal(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        gameboard[0, 1] = CellType.ICE
        with self.assertRaises(ValueError):
            my_gameboard.Find_Goal_Pos()


class Test__next_occupied_cell(unittest.TestCase):
    def test__next_occupied_cell_none(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))

        test_arr = np.empty((10,), dtype=cell_dtype)
        test_arr.fill(CellType.ICE)
        cell_type, loc = my_gameboard._next_occupied_cell(test_arr, 0)
        self.assertEqual(cell_type, CellType.BORDER)
        self.assertEqual(loc, len(test_arr))


    def test__next_occupied_cell_block_4(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))


        test_arr = np.empty((10,), dtype=cell_dtype)
        test_arr.fill(CellType.ICE)
        test_arr[4] = CellType.BLOCK
        cell_type, loc = my_gameboard._next_occupied_cell(test_arr, 0)
        self.assertEqual(cell_type, CellType.BLOCK)
        self.assertEqual(loc, 4)

    def test__next_occupied_cell_block_4_start5(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))

        test_arr = np.empty((10,), dtype=cell_dtype)
        test_arr.fill(CellType.ICE)
        test_arr[4] = CellType.BLOCK
        cell_type, loc = my_gameboard._next_occupied_cell(test_arr, 5)
        self.assertEqual(cell_type, CellType.BORDER)
        self.assertEqual(loc, len(test_arr))

    def test__next_occupied_cell_block_4_start5_goal(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))

        test_arr = np.empty((10,), dtype=cell_dtype)
        test_arr.fill(CellType.ICE)
        test_arr[8] = CellType.GOAL
        cell_type, loc = my_gameboard._next_occupied_cell(test_arr, 5)
        self.assertEqual(cell_type, CellType.GOAL)
        self.assertEqual(loc, 8)

class Test_isGameBoardReady(unittest.TestCase):

    def test_isGameBoardReady_ready(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.UpdateCell(Cell(1,1), CellType.BLOCK)
        my_gameboard.SetPlayerPos(Cell(2,2))
        self.assertTrue(my_gameboard.isGameBoardReady())

    def test_isGameBoardReady_missing_goal(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        gameboard[0, 1] = CellType.ICE
        my_gameboard.UpdateCell(Cell(1,1), CellType.BLOCK)
        my_gameboard.SetPlayerPos(Cell(2,2))
        self.assertFalse(my_gameboard.isGameBoardReady())

    def test_isGameBoardReady_missing_blocked(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        self.assertFalse(my_gameboard.isGameBoardReady())
    def test_isGameBoardReady_missing_player(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.player_pos = None
        self.assertFalse(my_gameboard.isGameBoardReady())

    def test_isGameBoardReady_missing_all(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.player_pos = None
        gameboard[0, 1] = CellType.ICE
        self.assertFalse(my_gameboard.isGameBoardReady())

class Test_NextBlock(unittest.TestCase):
    def test_NextBlock_blocked_down_0_4(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.player_pos = Cell(0, 0)
        cell_type, loc = my_gameboard.NextBlock(Direction.DOWN)
        self.assertEqual(cell_type, CellType.BLOCK)
        self.assertEqual(loc, Cell(row=4, col=0))


    def test_NextBlock_blocked_up_3_2(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(9, 2))
        cell_type, loc = my_gameboard.NextBlock(Direction.UP)
        self.assertEqual(cell_type, CellType.BLOCK)
        self.assertEqual(loc, Cell(row=3, col=2))

    def test_NextBlock_blocked_right_3_9(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(9, 2))
        cell_type, loc = my_gameboard.NextBlock(Direction.RIGHT)
        self.assertEqual(cell_type, CellType.BLOCK)
        self.assertEqual(loc, Cell(row=9, col=3))

    def test_NextBlock_blocked_left_0_9(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(9, 2))
        cell_type, loc = my_gameboard.NextBlock(Direction.LEFT)
        self.assertEqual(cell_type, CellType.BLOCK)
        self.assertEqual(loc, Cell(row=9, col=0))

    def test_NextBlock_border_up_4_neg1(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
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
        my_gameboard.SetPlayerPos(Cell(5, 4))
        cell_type, loc = my_gameboard.NextBlock(Direction.UP)
        self.assertEqual(cell_type, CellType.BORDER)
        self.assertEqual(loc, Cell(row=-1, col=4))

    def test_NextBlock_border_down_5_10(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
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
        my_gameboard.SetPlayerPos(Cell(5, 5))
        cell_type, loc = my_gameboard.NextBlock(Direction.DOWN)
        self.assertEqual(cell_type, CellType.BORDER)
        self.assertEqual(loc, Cell(row=10, col=5))

    def test_NextBlock_border_left_neg1_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(0, 5))
        cell_type, loc = my_gameboard.NextBlock(Direction.LEFT)
        self.assertEqual(cell_type, CellType.BORDER)
        self.assertEqual(loc, Cell(row=0, col=-1))

    def test_NextBlock_border_right_10_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(0, 5))
        cell_type, loc = my_gameboard.NextBlock(Direction.RIGHT)
        self.assertEqual(cell_type, CellType.BORDER)
        self.assertEqual(loc, Cell(row=0, col=10))

    def test_NextBlock_border_right_10_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(0, 5))
        cell_type, loc = my_gameboard.NextBlock(Direction.RIGHT)
        self.assertEqual(cell_type, CellType.BORDER)
        self.assertEqual(loc, Cell(row=0, col=10))

    def test_NextBlock_goal_up_0_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.GOAL, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(8, 0))
        cell_type, loc = my_gameboard.NextBlock(Direction.UP)
        self.assertEqual(cell_type, CellType.GOAL)
        self.assertEqual(loc, Cell(row=0, col=0))

    def test_NextBlock_goal_down_9_9(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(2, 9))
        cell_type, loc = my_gameboard.NextBlock(Direction.DOWN)
        self.assertEqual(cell_type, CellType.GOAL)
        self.assertEqual(loc, Cell(row=9, col=9))

    def test_NextBlock_goal_right_9_9(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(9, 6))
        cell_type, loc = my_gameboard.NextBlock(Direction.RIGHT)
        self.assertEqual(cell_type, CellType.GOAL)
        self.assertEqual(loc, Cell(row=9, col=9))
    def test_NextBlock_goal_left_0_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.GOAL, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(0, 1))
        cell_type, loc = my_gameboard.NextBlock(Direction.LEFT)
        self.assertEqual(cell_type, CellType.GOAL)
        self.assertEqual(loc, Cell(row=0, col=0))


    def test_NextBlock_goal_up_0_0_0(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.GOAL, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(1, 0))
        cell_type, loc = my_gameboard.NextBlock(Direction.UP)
        self.assertEqual(cell_type, CellType.GOAL)
        self.assertEqual(loc, Cell(row=0, col=0))


class Test_MovePlayer(unittest.TestCase):
    def test_MovePlayer_right_border(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(0, 0))
        new_pos = my_gameboard.MovePlayer(Direction.RIGHT)
        self.assertEqual(new_pos, Cell(0, 9))


    def test_MovePlayer_down_blocked(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(0, 0))
        new_pos = my_gameboard.MovePlayer(Direction.DOWN)
        self.assertEqual(new_pos, Cell(3, 0))

    def test_MovePlayer_right_goal(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(0, 0))
        new_pos = my_gameboard.MovePlayer(Direction.RIGHT)
        self.assertEqual(new_pos, Cell(0, 4))

    def test_MovePlayer_left_blocked(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(8, 6))
        new_pos = my_gameboard.MovePlayer(Direction.LEFT)
        self.assertEqual(new_pos, Cell(8, 6))

    def test_MovePlayer_up_border(self):
        gameboard = np.empty((10, 10), dtype=cell_dtype)
        gameboard.fill(CellType.ICE)
        gameboard[0, 1] = CellType.GOAL
        my_gameboard = GameBoard(gameboard, Cell(0, 0))
        my_gameboard.gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.GOAL, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        my_gameboard.SetPlayerPos(Cell(8, 6))
        new_pos = my_gameboard.MovePlayer(Direction.UP)
        self.assertEqual(new_pos, Cell(0, 6))

#MovePlayer

if __name__ == '__main__':
    unittest.main()