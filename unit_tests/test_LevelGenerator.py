import unittest
import sys
import os
import numpy as np
#necessary to import things from the modules folder
sys.path.append(os.getcwd())
from modules.DataTypes import Point
from LevelGenerator import LevelGenerator
from modules.GameEnums import GameDifficulty, CellType
cell_dtype = np.dtype(CellType)
class Test_Constructor(unittest.TestCase):
    def test_Constructor_Beginner(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        self.assertTrue(True)

    def test_calculate_block_probability_0(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        generator.block_probability = 0.1
        generator.probability_increase_ratio = 1.8
        prob = generator.calculate_block_probability(0)
        self.assertEqual(prob, 0.1)

    def test_calculate_block_probability_1(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        generator.block_probability = 0.1
        generator.probability_increase_ratio = 1.8
        prob = generator.calculate_block_probability(1)
        self.assertEqual(prob, 0.6)

    
    def test_calculate_block_probability_2(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        generator.block_probability = 0.1
        generator.probability_increase_ratio = 1.8
        prob = generator.calculate_block_probability(2)
        self.assertEqual(prob, 0.8222222222222222222)

    def test_calculate_block_probability_7(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        generator.block_probability = 0.1
        generator.probability_increase_ratio = 1.8
        prob = generator.calculate_block_probability(7)
        self.assertEqual(prob, 0.9969170613482965)
    def test_calculate_block_probability_100(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        generator.block_probability = 0.1
        generator.probability_increase_ratio = 1.8
        prob = generator.calculate_block_probability(100)
        self.assertEqual(prob, 1)

    def test_count_neighboors_0(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
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
        num = generator.count_neighbors(gameboard, Point(x=1, y=1), CellType.BLOCK)
        self.assertEqual(num, 0)

    def test_count_neighboors_1(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
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
        num = generator.count_neighbors(gameboard, Point(x=1, y=1), CellType.BLOCK)
        self.assertEqual(num, 1)

    def test_count_neighboors_2(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
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
        num = generator.count_neighbors(gameboard, Point(x=1, y=1), CellType.BLOCK)
        self.assertEqual(num, 2)

    def test_count_neighboors_8(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        num = generator.count_neighbors(gameboard, Point(x=1, y=1), CellType.BLOCK)
        self.assertEqual(num, 8)

    def test_count_neighboors_top_left(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],
            [CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        num = generator.count_neighbors(gameboard, Point(x=0, y=0), CellType.BLOCK)
        self.assertEqual(num, 2)

    def test_count_neighboors_bottom_right(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK,],
            [CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.BLOCK, CellType.ICE,],
            [CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE, CellType.ICE,],     
        ], dtype=cell_dtype)
        num = generator.count_neighbors(gameboard, Point(x=9, y=9), CellType.BLOCK)
        self.assertEqual(num, 1)


    def test_random_goal_pos(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        goal_pos = generator.random_goal_pos(gameboard)
        self.assertEqual(goal_pos, Point(1, 9))


    def test_random_goal_pos_33(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.GOAL, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        goal_pos = generator.random_goal_pos(gameboard)
        self.assertEqual(goal_pos, Point(3, 3))

    def test_random_player_pos_33(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        gameboard = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.ICE, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.GOAL, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],     
        ], dtype=cell_dtype)
        player_pos = generator.random_player_pos(gameboard)
        self.assertEqual(player_pos, Point(3, 3))

if __name__ == '__main__':
    unittest.main()