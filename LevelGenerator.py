from modules.GameEnums import GameDifficulty, CellType, Game_Difficult_Str_Map_Reverse
from modules.configs import Board_Size_Lookup
from modules.GameBoard import GameBoard
from modules.LevelIO import LevelIO
import numpy as np
from modules.DataTypes import Point
import random

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

    def calculate_block_probability(self, num_adjacent_blocks: int) -> float:
        """
        Given the number of neighbors that as cell has of the same type, calculate the probability that that cell will also be that type.
        """
        probability = self.block_probability
        for i in range(num_adjacent_blocks):
            probability += (1-probability)/self.probability_increase_ratio
        return min(probability, 1.0)
    
    def count_neighbors(self, board: np.ndarray, location: Point, cell_type: CellType) -> int:
        """
        This method counts the number of neighbors that have the same cell type as the given `cell_type`. 
        """
        num_neighbors = 0
        width, height = board.shape
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i==0 and j==0:
                    continue
                if location.y+i>=height or location.y+i<0:
                    continue
                if location.x+j>=height or location.x+j<0:
                    continue
                if board[location.y+i, location.x+j] == cell_type:
                    num_neighbors += 1
        return num_neighbors

    def random_goal_pos(self, board: np.ndarray) -> Point:
        width, height = board.shape
        possible_positions = []
        for col in range(width):
            for row in range(height):
                if board[col, row] == CellType.ICE:
                    possible_positions.append(Point(row, col))
        idx = np.random.randint(0, len(possible_positions))
        return possible_positions[idx]

    def random_player_pos(self, board: np.ndarray) -> Point:
        width, height = board.shape
        possible_positions = []
        for col in range(width):
            for row in range(height):
                if board[col, row] == CellType.ICE:
                    possible_positions.append(Point(row, col))
        idx = np.random.randint(0, len(possible_positions))
        return possible_positions[idx]

    def generate(self, random_seed: int = None) -> GameBoard:
        np.random.seed(random_seed)
        board = self.empty_board.copy()
        width, height = board.shape
        all_board_locations = []
        for col in range(width):
            for row in range(height):
                all_board_locations.append(Point(row, col))
        random.shuffle(all_board_locations)
        for loc in all_board_locations:
            num_neighbors = self.count_neighbors(board, loc, CellType.BLOCK)
            prob = self.calculate_block_probability(num_neighbors)
            if np.random.binomial(1, prob):
                board[loc.y, loc.x] = CellType.BLOCK

        goal_pos = self.random_goal_pos(board)
        board[goal_pos.y, goal_pos.x] = CellType.GOAL
        player_pos = self.random_player_pos(board)
        return GameBoard(board, player_pos)



if __name__=="__main__":
    difficulty = GameDifficulty.BEGINNER
    generator = LevelGenerator(difficulty)
    generator.block_probability = 0.05
    generator.probability_increase_ratio = 2
    level_manager = LevelIO()
    level_manager.current_level = Game_Difficult_Str_Map_Reverse[difficulty]

    for i in range(3):
        level = generator.generate()
        level_manager.SaveNew(level)

