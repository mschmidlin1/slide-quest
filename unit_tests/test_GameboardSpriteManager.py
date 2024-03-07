import unittest
from SQ_modules.GameboardSpriteManager import Sprite_To_CellType, CellType_To_Sprite
from SQ_modules.Sprites import Player, Goal, Block, Ice
from SQ_modules.GameEnums import CellType, GameDifficulty
from SQ_modules.DataTypes import Cell





class Test_CellType_To_Sprite(unittest.TestCase):
    def test_player(self):
        result = CellType_To_Sprite(CellType.PLAYER)
        my_player_sprite = result(Cell(0, 0) , GameDifficulty.BEGINNER)
        self.assertEqual(result, Player)
        self.assertEqual(type(my_player_sprite), Player)

    def test_goal(self):
        result = CellType_To_Sprite(CellType.GOAL)
        my_sprite = result(Cell(0, 0) , GameDifficulty.BEGINNER)
        self.assertEqual(result, Goal)
        self.assertEqual(type(my_sprite), Goal)

class Test_Sprite_To_CellType(unittest.TestCase):
    def test_player(self):
        result = Sprite_To_CellType(Player)
        self.assertEqual(result, CellType.PLAYER)
    def test_block(self):
        block = Block(Cell(0, 0), GameDifficulty.BEGINNER)
        result = Sprite_To_CellType(type(block))
        self.assertEqual(result, CellType.BLOCK)

if __name__ == '__main__':
    unittest.main()