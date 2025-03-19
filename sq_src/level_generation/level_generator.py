from sq_src.data_structures.game_enums import GameDifficulty, CellType, Game_Difficult_Str_Map_Reverse, Direction
from sq_src.configs import Board_Size_Lookup
from sq_src.core.game_board import GameBoard
from sq_src.level_generation.level_io import LevelIO
from sq_src.data_structures.algorithms import ReachablePositions, ShortestPath
from sq_src.level_generation.level_io import LevelIO, MapgenIO
import numpy as np
from sq_src.data_structures.data_types import Cell
import random
import os
import copy
import collections
from sq_src.singletons.my_logging import LoggingService
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
        self.logging_service = LoggingService()
        self.difficulty = difficulty
        self.board_dimensions = Board_Size_Lookup[difficulty]
        self.block_probability = 0.05 #increase this number to increase number of blobs
        self.feature_probability = 0.2
        self.probability_increase_ratio = 1.65 #decrease this number to increase size of blobs
        self.empty_board = np.empty(self.board_dimensions, dtype=cell_dtype)
        self.empty_board.fill(CellType.ICE)
        self.resources = MapgenIO.ReadMapgen()
    
    def calculate_block_probability(self, num_adjacent_blocks: int) -> float:
        """
        Given the number of neighbors that as cell has of the same type, calculate the probability that that cell will also be that type.
        """
        probability = self.block_probability
        for i in range(num_adjacent_blocks):
            probability += (1-probability)/self.probability_increase_ratio
        return min(probability, 1.0)
    
    def count_neighbors(self, board: np.ndarray, location: Cell, cell_type: CellType) -> int:
        """
        This method counts the number of neighbors that have the same cell type as the given `cell_type`. 
        """
        num_neighbors = 0
        width, height = board.shape
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i==0 and j==0:
                    continue
                if location.row+i>=height or location.row+i<0:
                    continue
                if location.col+j>=height or location.col+j<0:
                    continue
                if board[location.row+i, location.col+j] == cell_type:
                    num_neighbors += 1
        return num_neighbors
    
    def random_goal_pos(self, board: np.ndarray, rng: np.random.RandomState) -> Cell:
        """
        Selects a random goal position from the board where the cell type is ICE using a specified random number generator.

        Iterates over the board to identify positions marked as ICE. Utilizes the provided random number generator (rng) 
        to randomly select one of these positions to be the goal. If no ICE cells are found, returns None.

        Parameters:
        - board (np.ndarray): A 2D numpy array representing the game board, where each cell's value corresponds to a CellType enum.
        - rng (np.random.RandomState): A RandomState instance for reproducible random operations.

        Returns:
        Cell: A randomly selected Cell object (row, column) representing the goal position on the ICE cells. Returns None if no ICE cells are found.
        """
        width, height = board.shape
        possible_goal_positions = []
        for col in range(width):
            for row in range(height):
                if board[row, col] == CellType.ICE:
                    possible_goal_positions.append(Cell(row=row, col=col))
        if len(possible_goal_positions)==0:
            return None
        idx = rng.randint(0, len(possible_goal_positions))
        return possible_goal_positions[idx]
    
    def random_player_pos(self, board: np.ndarray, rng: np.random.RandomState) -> Cell:
        """
        Selects a random player position from the board where the cell type is ICE, ensuring it does not coincide with the goal position, using a specified random number generator.

        Identifies all possible ICE positions on the board and uses the provided random number generator (rng) to randomly 
        select one for the player. Validates that this position is not the same as the goal position. If no valid ICE cells 
        are found or the selected position is the goal position, returns None or raises a ValueError, respectively.

        Parameters:
        - board (np.ndarray): A 2D numpy array representing the game board, with cell values corresponding to a CellType enum.
        - rng (np.random.RandomState): A RandomState instance for reproducible random selections.

        Returns:
        Cell: A randomly selected Cell object (row, column) for the player's position. Returns None if no ICE cells are found.

        Raises:
        ValueError: If the randomly selected player position coincides with the goal position.
        """
        temp_gameboard = GameBoard(board, Cell(0, 0), 0)
        width, height = board.shape
        possible_player_positions = []
        for col in range(width):
            for row in range(height):
                if board[row, col] == CellType.ICE:
                    possible_player_positions.append(Cell(row, col))
        if len(possible_player_positions)==0:
            return None
        idx = rng.randint(0, len(possible_player_positions))
        if possible_player_positions[idx]==temp_gameboard.goal_pos:
            raise ValueError("player position was found to be goal position.")
        return possible_player_positions[idx]
    
    def contains(self, list1: list, list2: list) -> bool:
        """
        Determins if all the elements of list1 are contained in list2.
        """
        return set(list1).issubset(set(list2))
    
    def insert_feature(self, loc: Cell, feature: np.ndarray, board: np.ndarray) -> np.ndarray:
        """
        Inserts a rectangular feature into a copy of the game board at a specified location and returns the copy.

        The feature is placed with its upper-left corner at the (x, y) coordinates specified by `loc`.
        This creates and modifies a copy of the `board`, overlaying the specified section with the `feature`,
        and returns the modified copy.

        Parameters:
        - loc (Cell): Coordinates (x=row, y=column) for the upper-left corner where the feature begins.
        - feature (np.ndarray): 2D numpy array of the feature to insert. Assumed to be rectangular.
        - board (np.ndarray): 2D numpy array representing the game board. Not modified.

        Returns:
        np.ndarray: A modified copy of the game board with the feature inserted.
        """
        if len(feature.shape) != 2:
            raise ValueError(f"feature array has shape length of {len(feature.shape)} and not length 2.")
        if len(board.shape) != 2:
            raise ValueError(f"board array has shape length of {len(board.shape)} and not length 2.")
        
        if not all(inner_dim <= outer_dim for inner_dim, outer_dim in zip(feature.shape, board.shape)):
            raise ValueError(f"Feature does not fit inside of board.")
        # Create a copy of the game board to avoid modifying the original
        board_copy = np.copy(board)
        
        # Calculate the number of rows and columns in the feature
        nrows, ncols = feature.shape
        
        # Insert the feature into the copied game board
        board_copy[loc.row:loc.row+nrows, loc.col:loc.col+ncols] = feature
        
        return board_copy
    
    def get_covered_points(self, loc: Cell, feature: np.ndarray) -> list[Cell]:
        """
        Computes and returns a list of Cells covered by a rectangular feature placed on the gameboard,
        excluding the top-left corner point. 

        Parameters:
        - loc (Cell): The top-left corner (x=row, y=column) of the feature on the gameboard.
        - feature (np.ndarray): A 2D numpy array representing the rectangular feature's dimensions. Cannot by empty!

        Returns:
        list[Cell]: A list of Cells covered by the feature, excluding the initial top-left corner point.
        """
        if len(feature.shape) != 2:
            raise ValueError(f"feature array has shape length of {len(feature.shape)} and not length 2.")
        nrows, ncols = feature.shape
        points = []
        for row_num in range(loc.row, loc.row+nrows):
            for col_num in range(loc.col, loc.col+ncols):
                points.append(Cell(row_num, col_num))
        points.remove(loc)
        return points
    
    def generate_candidate(self, random_seed: int = None) -> GameBoard:
        """
        Generates a random game board with features, blocks, a goal, and a player position based on specified probabilities.

        This method initializes the random seed for reproducibility, copies an empty board template, and randomly distributes features (from predefined resources) and blocks across the board. It then sets a goal position and a player position, ensuring they do not coincide. The generation process respects the constraints of feature placement and boundary conditions.

        Parameters:
        - random_seed (int, optional): Seed for the random number generators to ensure reproducible results. Default is None, which does not seed the generator.

        Returns:
        GameBoard: An instance of the GameBoard class representing the generated game board, populated with features, blocks, a goal, and a player position. Returns None if it's impossible to place either the goal or the player.

        Notes:
        - The method uses internal probabilities (`feature_probability`, `block_probability`) to decide on placing features and blocks.
        - It ensures that features do not overlap and that the player and goal positions are valid and distinct.
        - Logs are generated for tracking the generation process and any potential errors in placement.
        """
        self.logging_service.log_info(f"Generating random map with seed: {random_seed}")
        rng = np.random.RandomState(random_seed)
        board = self.empty_board.copy()
        width, height = board.shape
        all_board_locations: list[Cell] = []
        for col in range(width):
            for row in range(height):
                all_board_locations.append(Cell(row, col))
        rng.shuffle(all_board_locations)
        while len(all_board_locations)>0:#iterate until all the board positions have been considered.
            loc = all_board_locations.pop()#remove the last location in the list
            if rng.binomial(1, self.feature_probability): #binomial choice based on feature probability
                feature = self.resources[rng.choice(list(self.resources.keys()))] #randomly select a feature from those available in "mapgen_resources" folder
                needed_locations = self.get_covered_points(loc, feature)

                if self.contains(needed_locations, all_board_locations): #make sure all the points the feature needs are still available, this also checks the boundries.
                    #remove all the needed_locations from the all_board_locations so they can't be used again
                    for needed_loc in needed_locations:
                        all_board_locations.remove(needed_loc)
                    #replace all the relevant points with the feature
                    board = self.insert_feature(loc, feature, board)
            # if loc not selected for a feature
            elif rng.binomial(1, self.block_probability):
                board[loc.row, loc.col] = CellType.BLOCK
            else:
                pass#the location remains ice

        goal_pos = self.random_goal_pos(board, rng)
        if goal_pos is None:
            return None
        self.goal_pos = goal_pos
        board[goal_pos.row, goal_pos.col] = CellType.GOAL
        player_pos = self.random_player_pos(board, rng)
        if player_pos is None:
            return None
        if player_pos == goal_pos:
            self.logging_service.log_info(f"Goal position and player position both have location: {player_pos}")
        gameboard = GameBoard(board, player_pos, random_seed)
        if gameboard.player_pos == gameboard.Find_Goal_Pos():
            self.logging_service.log_info(f"Goal position and player position both have location: {gameboard.player_pos}")
        return gameboard


    def generate(self, starting_num=0) -> tuple[int, GameBoard]:
        """
        Generates a valid game board along with its seed.

        This method repeatedly attempts to generate a game board using random seeds until it finds a configuration where both the player and goal positions are set, and the map is solvable (i.e., there exists a path between the player and goal).
        In addition, it must take at least 2 moves to solve the map.
        It first checks the "starting_num" as a seed and indexes by 1 until a valid seed is found.

        Returns:
        tuple[int, GameBoard]: A tuple containing the seed used to generate the playable game board and the game board itself.
        """
        candidate_seed = starting_num - 1
        while True:
            candidate_seed += 1
            candidate = self.generate_candidate(candidate_seed)
            if candidate is None:
                self.logging_service.log_info(f"Candidate failed as player or goal position could not be found.(seed={candidate_seed})")
                continue

            if len(ShortestPath(candidate)) < 3:
                self.logging_service.log_info(f"Candidate map failed.(seed={candidate_seed})")
                continue

            player_pos = candidate.player_pos  # save player position for after this check
            goal_pos = candidate.goal_pos
            reachable_positions = ReachablePositions(candidate)
            for position in reachable_positions:
                if position in [player_pos, goal_pos]:#don't bother checking for player pos and goal position
                    continue
                candidate.SetPlayerPos(position)
                if len(ShortestPath(candidate)) < 1:  # check to see if map is possible from this position
                    self.logging_service.log_info(f"Candidate map failed from position {position}.(seed={candidate_seed})")
                    break # break the inner loop and continue the outer loop

            else: #if the inner for loop finishes without breaking
                candidate.SetPlayerPos(player_pos)
                return (candidate_seed, candidate)
            
            #if the for loop broke, continue the outer while loop.
            continue


    

