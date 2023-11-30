import unittest
import sys
import os
import numpy as np
#necessary to import things from the modules folder
sys.path.append(os.getcwd())
from LevelGenerator import LevelGenerator
from modules.GameEnums import GameDifficulty

class Test_Constructor(unittest.TestCase):
    def test_Constructor_Beginner(self):
        generator = LevelGenerator(difficulty=GameDifficulty.BEGINNER)
        self.assertTrue(True)





if __name__ == '__main__':
    unittest.main()