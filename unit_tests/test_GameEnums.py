import unittest
import sys
import os
import numpy as np
#necessary to import things from the SQ_modules folder
sys.path.append(os.getcwd())
from SQ_modules.GameBoard import GameBoard
from SQ_modules.GameEnums import Direction, CellType, Str_to_CellType, Str_to_CellType_func, Str_to_CellType_vector_func
from SQ_modules.DataTypes import Point

class Test_Str_to_CellType(unittest.TestCase):

    def test_Str_to_CellType_len(self):
        self.assertEqual(len(Str_to_CellType), 8)

    def test_Str_to_CellType_members(self):
        keys = list(Str_to_CellType.keys())
        self.assertEqual(keys[0], 'CellType.ICE')
        self.assertEqual(keys[1], 'CellType.BLOCK')
        self.assertEqual(keys[2], 'CellType.PLAYER')
        self.assertEqual(keys[3], 'CellType.GOAL')
        self.assertEqual(keys[4], 'CellType.PORTAL')
        self.assertEqual(keys[5], 'CellType.POWER_UP')
        self.assertEqual(keys[6], 'CellType.BORDER')
        self.assertEqual(keys[7], 'CellType.GROUND')

class Test_Str_to_CellType(unittest.TestCase):
    def test_Str_to_CellType_func(self):
        self.assertEqual(Str_to_CellType_func('CellType.ICE'), CellType.ICE)
        self.assertEqual(Str_to_CellType_func('CellType.GOAL'), CellType.GOAL)
        self.assertEqual(Str_to_CellType_func('CellType.GROUND'), CellType.GROUND)

class Test_Str_to_CellType_vector_func(unittest.TestCase):
    def test_Str_to_CellType_vector_func(self):
        cell_dtype = np.dtype(CellType)
        custom_string_dtype = np.dtype(f"S{50}")
        array = np.empty(10, dtype=custom_string_dtype)
        array.fill("CellType.ICE")
        array = array.astype(str)
        converted_array = Str_to_CellType_vector_func(array)
        self.assertEqual(converted_array[0], CellType.ICE)

if __name__ == '__main__':
    unittest.main()