from sq_src.core.game_board import GameBoard
from sq_src.level_generation.level_generator import LevelGenerator
from sq_src.metas import SingletonMeta
from sq_src.level_generation.seed import Seed
from sq_src.data_structures.game_enums import GameDifficulty, Direction
from sq_src.data_structures.algorithms import ShortestPath
from sq_src.singletons.user_data import UserData
from sq_src.singletons.my_logging import LoggingService




class LevelManager(metaclass=SingletonMeta):
    """
    The level manager class is responsible for managing the different map seeds.

    Methods:
        - load_level() : loads the next level
        - save_seed()  : saves a seed to user_data
        - next_seed()  : determines which seed is next using level_generator
        - get_current_gameboard() : gets the current gameboard object
    """
    current_seed: Seed
    level_generator: LevelGenerator
    current_difficulty: GameDifficulty
    user_data: UserData
    current_gameboard: GameBoard
    def __init__(self):
        self.current_difficulty = None
        self.user_data = UserData()
        self.logging_service = LoggingService()


    def load_level(self, new_difficulty: GameDifficulty):
        """
        Set the difficulty.
        Load the level.
        Find the next level if the current one is complete.
        """
        self.logging_service.log_info(f"Loading difficulty {new_difficulty}.")
        self.current_difficulty = new_difficulty
        self.level_generator = LevelGenerator(new_difficulty)
        self.current_seed = self.user_data.get_current_seed(new_difficulty)
        if self.current_seed.completed:
            self.next_seed()
        else:
            self.current_gameboard = self.level_generator.generate_candidate(self.current_seed.number)

    
    def save_seed(self, shortest_path: Direction, completed: bool, time_ms: float, num_moves: int):
        """
        Saves the seed data after completion of the map.

        - shortest_path: optimal path to complete the map.
        - completed: whether or not the map was completed.
        - time_ms: how long it took to complete the map.
        - num_moves: the number of moves it took to complete the map.
        """
        seed_to_save = Seed(self.current_seed.number, shortest_path, completed, True, time_ms, num_moves)
        self.logging_service.log_info(f"Saving map seed: {seed_to_save}")
        self.current_seed = seed_to_save
        self.user_data.set_current_seed(self.current_difficulty, seed_to_save)
        self.user_data.replace_map(self.current_difficulty, seed_to_save)

    def next_seed(self):
        """
        Finds the next playable seed and stores it as the current gameboard.
        """
        new_seed, gameboard = self.level_generator.generate(self.current_seed.number+1)
        #add all the failed seeds to the user data for saving
        for i in range(self.current_seed.number+1, new_seed):
            failed_seed = Seed(i, [], False, False, 0, 0)
            self.user_data.replace_map(self.current_difficulty, failed_seed)
        
        self.current_seed = Seed(new_seed, ShortestPath(gameboard), False, True, 0, 0)
        self.user_data.replace_map(self.current_difficulty, self.current_seed)
        self.user_data.set_current_seed(self.current_difficulty, self.current_seed)
        self.current_gameboard = gameboard

    def get_current_gameboard(self) -> GameBoard:
        """
        Gets the current gameboard.
        """
        return self.current_gameboard
    




    

    