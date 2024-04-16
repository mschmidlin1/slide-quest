from SQ_modules.GameBoard import GameBoard
from SQ_modules.LevelGenerator import LevelGenerator
from SQ_modules.Metas import SingletonMeta
from SQ_modules.Seed import Seed
from SQ_modules.GameEnums import GameDifficulty, Direction
from SQ_modules.ShortestPath import ShortestPath
from SQ_modules.UserData import UserData







class LevelManager(metaclass=SingletonMeta):
    current_seed: Seed
    level_generator: LevelGenerator
    current_difficulty: GameDifficulty
    user_data: UserData
    current_gameboard: GameBoard
    def __init__(self):
        self.current_difficulty = None
        self.user_data = UserData()


    def change_difficulty(self, new_difficulty: GameDifficulty):
        """
        Change the difficulty used to generate maps.
        """
        self.current_difficulty = new_difficulty
        self.level_generator = LevelGenerator(new_difficulty)
        self.current_seed = self.user_data.get_current_seed(new_difficulty)
        self.current_gameboard = self.level_generator.generate_candidate(self.current_seed.number)

    
    def save_seed(self, shortest_path: Direction, completed: bool, time_ms: float, num_moves: int):
        """
        Saves the seed data after completion of the map.

        - shortest_path: optimal path to complete the map.
        - completed: whether or not the map was completed.
        - time_ms: how long it took to complete the map.
        - num_moves: the number of moves it took to complete the map.
        """
        self.user_data.replace_map(self.current_difficulty, Seed(self.current_seed.number, shortest_path, completed, True, time_ms, num_moves))

    def next_seed(self):
        """
        Finds the next playable seed and stores it as the current gameboard.
        """
        new_seed, gameboard = self.level_generator.generate(self.current_seed.number+1)
        #add all the failed seeds to the user data for saving
        for i in range(self.current_seed+1, new_seed):
            failed_seed = Seed(i, [], False, False, 0, 0)
            self.user_data.add_map(self.current_difficulty, failed_seed)
        
        self.current_seed = Seed(new_seed, ShortestPath(gameboard), False, True, 0, 0)
        self.user_data.set_current_seed(self.current_seed)
        self.current_gameboard = gameboard

    def get_current_gameboard(self) -> GameBoard:
        """
        Gets the current gameboard.
        """
        return self.current_gameboard
    




    

    