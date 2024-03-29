from SQ_modules.GameEnums import GameDifficulty, CellType, Game_Difficult_Str_Map_Reverse, Direction
from SQ_modules.configs import Board_Size_Lookup
from SQ_modules.GameBoard import GameBoard
from SQ_modules.LevelIO import LevelIO
from SQ_modules.ShortestPath import ShortestPath
from SQ_modules.LevelIO import LevelIO
import numpy as np
from SQ_modules.DataTypes import Point
import random
import os
import copy
import collections
from SQ_modules.my_logging import set_logger, log
import logging
import random
cell_dtype = np.dtype(CellType)
set_logger()


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
        self.feature_probability = 0.2
        self.probability_increase_ratio = 1.65 #decrease this number to increase size of blobs
        self.empty_board = np.empty(self.board_dimensions, dtype=cell_dtype)
        self.empty_board.fill(CellType.ICE)
        self.resources = self.read_mapgen_resources()
    @log
    def read_mapgen_resources(self) -> dict[str, np.ndarray]:
        """
        Reads the mapgen resources from files.

        Returns a dictionary where the keys are strings (file names) and the values are np.ndarrays of dtype CellType.
        """
        level_io = LevelIO()
        resource_files = os.listdir("mapgen_resources")
        resources = {}
        for file in resource_files:
            full_path = os.path.join("mapgen_resources", file)
            sub_map: np.ndarray = level_io.ReadBoard(full_path)
            resources[file] = sub_map
        return resources
    @log
    def calculate_block_probability(self, num_adjacent_blocks: int) -> float:
        """
        Given the number of neighbors that as cell has of the same type, calculate the probability that that cell will also be that type.
        """
        probability = self.block_probability
        for i in range(num_adjacent_blocks):
            probability += (1-probability)/self.probability_increase_ratio
        return min(probability, 1.0)
    @log
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
    @log
    def random_goal_pos(self, board: np.ndarray, rng: np.random.RandomState) -> Point:
        """
        Selects a random goal position from the board where the cell type is ICE using a specified random number generator.

        Iterates over the board to identify positions marked as ICE. Utilizes the provided random number generator (rng) 
        to randomly select one of these positions to be the goal. If no ICE cells are found, returns None.

        Parameters:
        - board (np.ndarray): A 2D numpy array representing the game board, where each cell's value corresponds to a CellType enum.
        - rng (np.random.RandomState): A RandomState instance for reproducible random operations.

        Returns:
        Point: A randomly selected Point object (row, column) representing the goal position on the ICE cells. Returns None if no ICE cells are found.
        """
        width, height = board.shape
        possible_goal_positions = []
        for col in range(width):
            for row in range(height):
                if board[col, row] == CellType.ICE:
                    possible_goal_positions.append(Point(row, col))
        if len(possible_goal_positions)==0:
            return None
        idx = rng.randint(0, len(possible_goal_positions))
        return possible_goal_positions[idx]
    @log
    def random_player_pos(self, board: np.ndarray, rng: np.random.RandomState) -> Point:
        """
        Selects a random player position from the board where the cell type is ICE, ensuring it does not coincide with the goal position, using a specified random number generator.

        Identifies all possible ICE positions on the board and uses the provided random number generator (rng) to randomly 
        select one for the player. Validates that this position is not the same as the goal position. If no valid ICE cells 
        are found or the selected position is the goal position, returns None or raises a ValueError, respectively.

        Parameters:
        - board (np.ndarray): A 2D numpy array representing the game board, with cell values corresponding to a CellType enum.
        - rng (np.random.RandomState): A RandomState instance for reproducible random selections.

        Returns:
        Point: A randomly selected Point object (row, column) for the player's position. Returns None if no ICE cells are found.

        Raises:
        ValueError: If the randomly selected player position coincides with the goal position.
        """
        temp_gameboard = GameBoard(board, Point(0, 0))
        width, height = board.shape
        possible_player_positions = []
        for col in range(width):
            for row in range(height):
                if board[col, row] == CellType.ICE:
                    possible_player_positions.append(Point(row, col))
        if len(possible_player_positions)==0:
            return None
        idx = rng.randint(0, len(possible_player_positions))
        if possible_player_positions[idx]==temp_gameboard.goal_pos:
            raise ValueError("player position was found to be goal position.")
        return possible_player_positions[idx]
    @log
    def contains(self, list1: list, list2: list) -> bool:
        """
        Determins if all the elements of list1 are contained in list2.
        """
        return set(list1).issubset(set(list2))
    @log
    def insert_feature(self, loc: Point, feature: np.ndarray, board: np.ndarray) -> np.ndarray:
        """
        Inserts a rectangular feature into a copy of the game board at a specified location and returns the copy.

        The feature is placed with its upper-left corner at the (x, y) coordinates specified by `loc`.
        This creates and modifies a copy of the `board`, overlaying the specified section with the `feature`,
        and returns the modified copy.

        Parameters:
        - loc (Point): Coordinates (x=row, y=column) for the upper-left corner where the feature begins.
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
        board_copy[loc.x:loc.x+nrows, loc.y:loc.y+ncols] = feature
        
        return board_copy
    @log
    def get_covered_points(self, loc: Point, feature: np.ndarray) -> list[Point]:
        """
        Computes and returns a list of Points covered by a rectangular feature placed on the gameboard,
        excluding the top-left corner point. 

        Parameters:
        - loc (Point): The top-left corner (x=row, y=column) of the feature on the gameboard.
        - feature (np.ndarray): A 2D numpy array representing the rectangular feature's dimensions. Cannot by empty!

        Returns:
        list[Point]: A list of Points covered by the feature, excluding the initial top-left corner point.
        """
        if len(feature.shape) != 2:
            raise ValueError(f"feature array has shape length of {len(feature.shape)} and not length 2.")
        nrows, ncols = feature.shape
        points = []
        for row_num in range(loc.x, loc.x+nrows):
            for col_num in range(loc.y, loc.y+ncols):
                points.append(Point(row_num, col_num))
        points.remove(loc)
        return points
    @log
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
        logging.info(f"Generating random map with seed: {random_seed}")
        rng = np.random.RandomState(random_seed)
        board = self.empty_board.copy()
        width, height = board.shape
        all_board_locations = []
        for col in range(width):
            for row in range(height):
                all_board_locations.append(Point(row, col))
        rng.shuffle(all_board_locations)
        while len(all_board_locations)>0:#iterate until all the board positions have been considered.
            loc = all_board_locations.pop()#remove the last location in the list
            if rng.binomial(1, self.feature_probability): #binomial choice based on feature probability
                feature = self.resources[rng.choice(self.resources.keys())] #randomly select a feature from those available in "mapgen_resources" folder
                needed_locations = self.get_covered_points(loc, feature)

                if self.contains(needed_locations, all_board_locations): #make sure all the points the feature needs are still available, this also checks the boundries.
                    #remove all the needed_locations from the all_board_locations so they can't be used again
                    for needed_loc in needed_locations:
                        all_board_locations.remove(needed_loc)
                    #replace all the relevant points with the feature
                    board = self.insert_feature(loc, feature, board)
            # if loc not selected for a feature
            elif rng.binomial(1, self.block_probability):
                board[loc.y, loc.x] = CellType.BLOCK
            else:
                pass#the location remains ice

        goal_pos = self.random_goal_pos(board, rng)
        if goal_pos is None:
            return None
        self.goal_pos = goal_pos
        board[goal_pos.y, goal_pos.x] = CellType.GOAL
        player_pos = self.random_player_pos(board, rng)
        if player_pos is None:
            return None
        if player_pos == goal_pos:
            logging.error(f"Goal position and player position both have location: {player_pos}")
        gameboard = GameBoard(board, player_pos)
        if gameboard.player_pos == gameboard.Find_Goal_Pos():
            logging.error(f"Goal position and player position both have location: {gameboard.player_pos}")
        return gameboard
    @log
    def generate(self) -> tuple[int, GameBoard]:
        """
        Generates a valid game board along with its seed.

        This method repeatedly attempts to generate a game board using random seeds until it finds a configuration where both the player and goal positions are set, and the map is solvable (i.e., there exists a path between the player and goal).

        Returns:
        tuple[int, GameBoard]: A tuple containing the seed used to generate the playable game board and the game board itself.

        Notes:
        - The method internally generates candidate game boards using randomly selected seeds within a predefined range.
        - It verifies each candidate to ensure that player and goal positions can be placed and that the map is not impossible to solve.
        - Upon finding a valid configuration, it returns the seed and the corresponding game board.
        """
        while True:
            candidate_seed = np.random.randint(0, 100000)
            candidate = self.generate_candidate(candidate_seed)
            if candidate is None:
                logging.info(f"Candidate failed as player or goal position could not be found.(seed={candidate_seed})")
                continue
            elif len(ShortestPath(candidate))==0:
                logging.info(f"Candidate failed as map is impossible.(seed={candidate_seed})")
                continue
            else:
                return (candidate_seed, candidate)


if __name__=="__main__":
    difficulty = GameDifficulty.HARD
    generator = LevelGenerator(difficulty)
    generator.block_probability = 0.25
    generator.probability_increase_ratio = 2
    generator.feature_probability = 0.4
    level_manager = LevelIO()
    level_manager.current_level = Game_Difficult_Str_Map_Reverse[difficulty]
    maps_created = 0
    while maps_created<4:
        level = generator.generate_candidate()
        if level:
            if level.player_pos == level.Find_Goal_Pos():
                print()
            if len(ShortestPath(level))>0:
                if level.player_pos == level.Find_Goal_Pos():
                    print()
                level_manager.SaveNew(level)
                maps_created+=1
                logging.info("Successfully created map.")
            else:
                logging.info("Map was impossible, failed to create map.")
        else:
            logging.info("Map was impossible, failed to create map.")

