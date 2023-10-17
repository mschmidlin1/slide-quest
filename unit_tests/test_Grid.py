import unittest
from modules.Grid import Grid

class TestGrid(unittest.TestCase):

    def test_multiply(self):
        self.assertEqual(multiply(1, 2), 1*2)

    def test_add(self):
        self.assertEqual(add(1, 2), 1+2)


if __name__ == '__main__':
    unittest.main()