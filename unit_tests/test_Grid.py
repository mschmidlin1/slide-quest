import unittest
import sys
import os
#necessary to import things from the modules folder
sys.path.append(os.getcwd())
from modules.Grid import Grid

class TestGrid(unittest.TestCase):

    def test_init(self):
        my_grid = Grid((4, 4))
        print(my_grid.grid)
        self.assertEqual(my_grid.grid.shape, (4, 4))




if __name__ == '__main__':
    unittest.main()