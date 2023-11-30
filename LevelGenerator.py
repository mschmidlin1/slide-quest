from modules.GameEnums import GameDifficulty, CellType
from modules.configs import Board_Size_Lookup
from modules.GameBoard import GameBoard
from modules.LevelIO import LevelIO
import numpy as np
from modules.DataTypes import Point

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
        self.block_probability = 0.05 #increase this number to increase number of blobs
        self.probability_increase_ratio = 1.65 #decrease this number to increase size of blobs
        self.empty_board = np.empty(self.board_dimensions, dtype=cell_dtype)
        self.empty_board.fill(CellType.ICE)


    def calculate_block_probability(self, num_adjacent_blocks: int):
        """
        Given the number of neighbors that as cell has of the same type, calculate the probability that that cell will also be that type.
        """
        probability = self.block_probability
        for i in range(num_adjacent_blocks):
            probability += (1-probability)/self.probability_increase_ratio
        return min(probability, 1.0)
    
    def count_neighbors(self, board: np.ndarray, location: Point, cell_type: CellType):
        """
        This method counts the number of neighbors that have the same cell type as the given `cell_type`. 
        """
        # num_neighbors = 0
        # [location.y, location.x]
        pass


    def generate(self, random_seed: int = None) -> GameBoard:
        pass



if __name__=="__main__":
    difficulty = GameDifficulty.BEGINNER
    generator = LevelGenerator(difficulty)
    level_manager = LevelIO()

    for i in range(10):
        level = generator.generate()
        level_manager.Save(level)

