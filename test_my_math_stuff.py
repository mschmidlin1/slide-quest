import unittest
from my_math_stuff import multiply, add, make_upper_case

class TestMymathstuff(unittest.TestCase):

    def test_multiply(self):
        self.assertEqual(multiply(1, 2), 1*2)

    def test_add(self):
        self.assertEqual(add(1, 2), 1+2)

    def test_uppercase(self):
        self.assertEqual(make_upper_case("my lower case string"), "MY LOWER CASE STRING")

if __name__ == '__main__':
    unittest.main()