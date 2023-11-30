from modules.GameEnums import GameDifficulty, CellType
from modules.configs import Board_Size_Lookup
from modules.GameBoard import GameBoard
from modules.LevelIO import LevelIO
import numpy as np

cell_dtype = np.dtype(CellType)

class LevelGenerator:
    """
    
    Ideas:
    ------

    - Generate blocks at random based on a probability
    - If there is a block adjacent increase the block probability (landscape generation)
    - Each adjacent block increases the probability that a given position will have a block
    
    - Once the gameboard is made, pick a random Ice spot to put the goal.
    - Starting from the goal location and using random directions, move away from the goal obeying the rules of the game. After an arbitrary number of moves, set your player location.

    
    
    """

    def __init__(self, difficulty: GameDifficulty):
        self.difficulty = difficulty
        self.board_dimensions = Board_Size_Lookup[difficulty]
        self.block_probability = 0.05
        self.probability_increase_ratio = 1.65
        self.empty_board = np.empty(self.board_dimensions, dtype=cell_dtype)
        self.empty_board.fill(CellType.ICE)


    def calculate_block_probability(self, num_adjacent_blocks: int):
        probability = self.block_probability
        for i in range(num_adjacent_blocks):
            probability += (1-probability)/self.probability_increase_ratio
        return probability


    def generate(self, random_seed: int = None) -> GameBoard:
        pass



if __name__=="__main__":
    difficulty = GameDifficulty.BEGINNER
    generator = LevelGenerator(difficulty)
    level_manager = LevelIO()

    for i in range(10):
        level = generator.generate()
        level_manager.Save(level)

