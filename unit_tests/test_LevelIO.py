import unittest
import sys
import os
import re
import numpy as np

sys.path.append(os.getcwd())
from sq_src.level_generation.level_io import LevelIO, eliminate_duplicates_dict

class Test_EliminateDuplicatesDict(unittest.TestCase):

    def test_empty_dict(self):
        self.assertEqual(eliminate_duplicates_dict({}), {})

    def test_all_unique(self):
        input_dict = {
            "path1": np.array([1, 2, 3]),
            "path2": np.array([4, 5, 6]),
        }
        self.assertEqual(eliminate_duplicates_dict(input_dict), input_dict)

    def test_all_duplicates(self):
        arr = np.array([1, 2, 3])
        input_dict = {
            "path1": arr,
            "path2": arr,
        }
        expected_dict = {
            "path1": arr,
        }
        self.assertEqual(eliminate_duplicates_dict(input_dict), expected_dict)

    def test_mixed_unique_and_duplicates(self):
        unique_arr1 = np.array([1, 2, 3])
        unique_arr2 = np.array([4, 5, 6])
        duplicate_arr = np.array([1, 2, 3])

        input_dict = {
            "path1": unique_arr1,
            "path2": duplicate_arr,  # Duplicate of path1
            "path3": unique_arr2,
        }
        expected_dict = {
            "path1": unique_arr1,
            "path3": unique_arr2,
        }
        self.assertEqual(eliminate_duplicates_dict(input_dict), expected_dict)

class Test_LevelIO(unittest.TestCase):
    def test_path_checking(self):
        level_manager = LevelIO()
        self.assertEqual(level_manager.levels_root_dir, "levels")

    def test_completed_file(self):
        level_manager = LevelIO()
        self.assertEqual(level_manager.completed_levels_file, "levels/#_completed.txt")

    def test_list_levels(self):
        level_manager = LevelIO()
        levels = level_manager.list_levels("administrative")
        self.assertEqual(levels, [])
    
    def test_regex_pattern_true(self):
        level_manager = LevelIO()
        self.assertTrue(re.match(level_manager.level_file_pattern, '3_2023-11-03 19.38.06.958190.csv'))

    def test_regex_pattern_false(self):
        level_manager = LevelIO()
        self.assertFalse(re.match(level_manager.level_file_pattern, '3_tttt-11-03 19.38.06.958190-player.csv'))

    def test_filter_by_completed(self):
        level_manager = LevelIO()
        incompleted_levels = level_manager.filter_by_completed(['a','b','c','d'], ['a', 'c'])
        self.assertEqual(incompleted_levels, ['b', 'd'])
    
    def test_get_player_file(self):
        level_manager = LevelIO()
        level_manager.current_level = 'this is a string'
        player_file = level_manager.get_player_file()
        self.assertEqual(player_file, 'this is a st-player.txt')

    def test_next_level(self):
        level_manager = LevelIO()
        current = level_manager.current_level
        current_len = len(level_manager.incomplete_levels)
        level_manager.next_level()
        new_level = level_manager.current_level
        new_len = len(level_manager.incomplete_levels)
        self.assertNotEqual(current, new_level)
        self.assertEqual(current_len-1, new_len)

    def test_clear_completed(self):
        level_manager = LevelIO()
        level_manager.clear_completed()
        self.assertEqual(len(level_manager.completed_levels), 0)

# class Test_MapgenIO(unittest.TestCase):
#     def test_path_checking(self):
#         level_manager = LevelIO()
#         self.assertEqual(level_manager.levels_root_dir, "levels")

if __name__ == '__main__':
    unittest.main()