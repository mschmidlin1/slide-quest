import unittest
import sys
import os
import numpy as np
#necessary to import things from the SQ_modules folder
sys.path.append(os.getcwd())
from SQ_modules.DataTypes import Point
from LevelGenerator import LevelGenerator
from SQ_modules.GameEnums import GameDifficulty, CellType
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
    def test_contins_both_empty(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        self.assertTrue(generator.contains([], []))
    def test_contins_1_empty(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        self.assertTrue(generator.contains([], [1, 2]))
    def test_contins_2_empty(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        self.assertFalse(generator.contains([1, 2], []))
    def test_contins_true(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        self.assertTrue(generator.contains([1, 2], [1, 2, 3, 4]))
    def test_contins_false(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        self.assertFalse(generator.contains([1, 2, 10], [1, 2, 3, 4]))

    def test_get_covered_points_4x4(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],  
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        covered_points = generator.get_covered_points(loc, feature)
        self.assertEqual(15, len(covered_points))
        self.assertIn(Point(1, 0), covered_points)
        self.assertIn(Point(3, 3), covered_points)
    def test_get_covered_points_empty(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([[]
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        with self.assertRaises(ValueError):
            covered_points = generator.get_covered_points(loc, feature)
    def test_get_covered_points_3x3(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],  
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        covered_points = generator.get_covered_points(loc, feature)
        self.assertEqual(8, len(covered_points))
        self.assertIn(Point(1, 0), covered_points)
        self.assertIn(Point(2, 2), covered_points)
    def test_get_covered_points_dimensions(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([CellType.ICE, CellType.BLOCK, CellType.BLOCK,
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        with self.assertRaises(ValueError):
            covered_points = generator.get_covered_points(loc, feature)
    def test_get_covered_points_3x5(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK,],
            [CellType.ICE, CellType.BLOCK, CellType.BLOCK,],  
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        covered_points = generator.get_covered_points(loc, feature)
        self.assertEqual(14, len(covered_points))
        self.assertIn(Point(1, 0), covered_points)
        self.assertIn(Point(2, 2), covered_points)
    def test_insert_feature_2x2(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([
            [CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK,],
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        board = np.array([
            [CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE,],
        ], dtype=cell_dtype)
        new_board = generator.insert_feature(loc, feature, board)
        self.assertEqual((2,2), new_board.shape)
        self.assertEqual(CellType.BLOCK, new_board[0,0])
        self.assertNotEqual(CellType.ICE, new_board[1,1])

    def test_insert_feature_empty(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        board = np.array([
            [CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE,],
        ], dtype=cell_dtype)

        with self.assertRaises(ValueError):
            new_board = generator.insert_feature(loc, feature, board)
    def test_insert_feature_doesnt_fit(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([            
            [CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE,],
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        board = np.array([
            [CellType.ICE, CellType.ICE,],
            [CellType.ICE, CellType.ICE,],
        ], dtype=cell_dtype)

        with self.assertRaises(ValueError):
            new_board = generator.insert_feature(loc, feature, board)
    def test_insert_feature_standard(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        feature = np.array([            
            [CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK,],
            [CellType.BLOCK, CellType.BLOCK,],
        ], dtype=cell_dtype)
        loc = Point(0, 0)
        board = np.array([
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
        new_board = generator.insert_feature(loc, feature, board)
        self.assertEqual((10,10), new_board.shape)
        self.assertEqual(CellType.BLOCK, new_board[0,0])
        self.assertNotEqual(CellType.ICE, new_board[1,1])
if __name__ == '__main__':
    unittest.main()