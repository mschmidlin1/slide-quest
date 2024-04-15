from SQ_modules.GameBoard import GameBoard
from SQ_modules.LevelGenerator import LevelGenerator
from SQ_modules.Metas import SingletonMeta
from SQ_modules.Seed import Seed
from SQ_modules.GameEnums import GameDifficulty
from SQ_modules.ShortestPath import ShortestPath
from SQ_modules.UserData import UserData







class LevelManager(metaclass=SingletonMeta):
    current_seed: Seed
    level_generator: LevelGenerator
    current_difficulty: GameDifficulty
    user_data: UserData
    current_gameboard: GameBoard
    def __init__(self, difficulty: GameDifficulty):
        self.current_difficulty = difficulty
        self.user_data = UserData()


    def change_difficulty(self, new_difficulty: GameDifficulty):
        self.current_difficulty = new_difficulty
        self.level_generator = LevelGenerator(new_difficulty)
        self.current_seed = self.user_data.get_current_seed(new_difficulty)
        self.current_gameboard = self.level_generator.generate_candidate(self.current_seed.number)

    
    def next_seed(self):
        """
        
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
        return self.current_gameboard
    




    

    