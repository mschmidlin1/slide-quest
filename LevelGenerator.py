from modules.GameEnums import GameDifficulty, CellType, Game_Difficult_Str_Map_Reverse, Direction
from modules.configs import Board_Size_Lookup
from modules.GameBoard import GameBoard
from modules.LevelIO import LevelIO
import numpy as np
from modules.DataTypes import Point
import random
from modules.queue import MyQueue
import copy
import collections
cell_dtype = np.dtype(CellType)

def ShortestPath(input_gameboard: GameBoard) -> list[Direction]:
    """
    This function takes in the gameboard and player position and will tell you
    the exact sequence of moves to complete the level in the minimum number of moves.

    If there is no possible path to the goal, and empty list is returned.

    This function deep copys the input gamebaord as to not manipulate it's state.

    This function uses Breadth First Search Algorithm (BFS).
    """

    gameboard = copy.deepcopy(input_gameboard)  # Use deepcopy if gameboard has nested objects
    queue = collections.deque()  # Use deque for efficient pops from the left
    queue.append((gameboard.player_pos, []))  # Start with the player position and an empty path
    goal_pos = gameboard.Find_Goal_Pos()
    visited = set()
    
    while queue:
        current_pos, path = queue.popleft()
        
        if current_pos == goal_pos:
            return path  # Return the path that led to the goal
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        
        for direction in Direction:
            gameboard.player_pos = current_pos
            next_pos = gameboard.MovePlayer(direction)
            
            # Check if next_pos is valid (not out of bounds or blocked)
            if next_pos!=current_pos and next_pos not in visited:
                # Append the current direction to the path and enqueue
                queue.append((next_pos, path + [direction]))
    
    return []  # Return an empty list if there's no path to the goal



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
        possible_goal_positions = []
        for col in range(width):
            for row in range(height):
                if board[col, row] == CellType.ICE:
                    possible_goal_positions.append(Point(row, col))
        idx = np.random.randint(0, len(possible_goal_positions))
        return possible_goal_positions[idx]

    def random_player_pos(self, board: np.ndarray) -> Point:
        temp_gameboard = GameBoard(board, Point(0, 0))
        width, height = board.shape
        possible_player_positions = []
        for col in range(width):
            for row in range(height):
                if board[col, row] == CellType.ICE:
                    possible_player_positions.append(Point(row, col))
        idx = np.random.randint(0, len(possible_player_positions))
        if possible_player_positions[idx]==temp_gameboard.goal_pos:
            raise ValueError("player position was found to be goal position.")
        return possible_player_positions[idx]

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
            # num_neighbors = self.count_neighbors(board, loc, CellType.BLOCK)
            # prob = self.calculate_block_probability(num_neighbors)
            if np.random.binomial(1, self.block_probability):
                board[loc.y, loc.x] = CellType.BLOCK

        goal_pos = self.random_goal_pos(board)
        self.goal_pos = goal_pos
        board[goal_pos.y, goal_pos.x] = CellType.GOAL
        player_pos = self.random_player_pos(board)
        if player_pos == goal_pos:
            print()
        gameboard = GameBoard(board, player_pos)
        if gameboard.player_pos == gameboard.Find_Goal_Pos():
            print()
        return gameboard



if __name__=="__main__":
    difficulty = GameDifficulty.HARD
    generator = LevelGenerator(difficulty)
    generator.block_probability = 0.25
    generator.probability_increase_ratio = 2
    level_manager = LevelIO()
    level_manager.current_level = Game_Difficult_Str_Map_Reverse[difficulty]
    maps_created = 0
    while maps_created<4:
        level = generator.generate()
        if level.player_pos == level.Find_Goal_Pos():
            print()
        if len(ShortestPath(level))>0:
            if level.player_pos == level.Find_Goal_Pos():
                print()
            level_manager.SaveNew(level)
            maps_created+=1
            print("Created Map")
        else:
            print("Failed Map")

