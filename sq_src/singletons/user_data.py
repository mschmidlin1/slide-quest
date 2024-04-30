from dataclasses import dataclass
from sq_src.level_generation.seed import Seed
from sq_src.metas import SingletonMeta
import os
from sq_src.configs import GAME_VOLUME
from sq_src.data_structures.game_enums import GameDifficulty, Direction
import pickle
from sq_src.my_logging import set_logger
import logging
set_logger()





class UserData(metaclass=SingletonMeta):
    """
    The UserData class reads and writes the serialized json data to track user settings and completed maps.
    """
    file_name: str = "save_data.pkl"
    music_volume: float
    sfx_volume: float
    seed_data: dict[GameDifficulty, set[Seed]]
    user_data: dict
    def __init__(self):
        self.seed_data = {difficulty: set() for difficulty in GameDifficulty}
        self.music_volume = GAME_VOLUME
        self.sfx_volume = GAME_VOLUME


        if not os.path.exists(self.file_name):
            self.user_data = {
                    "volume_levels": {
                        "music": self.music_volume,
                        "sfx": self.sfx_volume
                    },
                    "maps": self.seed_data,
                    "current_seed": {difficulty: Seed(0, [], False, False, 0, 0) for difficulty in GameDifficulty},
                    "user_name": "",
                }
            self.write()
        else:
            self.read()
    

    def write(self):
        """
        Saves the user data to file.
        """
        try:
            with open(self.file_name, 'wb') as f:
                pickle.dump(self.user_data, f)
        except IOError as e:
            logging.info(f"Error writing to file: {e}")

    def read(self):
        """
        Loads the user data from file.
        """
        try:
            with open(self.file_name, 'rb') as f:
                loaded_data = pickle.load(f)
                self.user_data = loaded_data
        except (IOError, EOFError, pickle.UnpicklingError) as e:
            logging.info(f"Error reading from file: {e}")
    
    def update_music_volume(self, volume: float):
        """
        Update the saved music volume.
        """
        self.user_data['volume_levels']['music'] = volume

    def update_sfx_volume(self, volume: float):
        """
        Update the saved sound effects volume.
        """
        self.user_data['volume_levels']['sfx'] = volume

    def add_map(self, difficulty: GameDifficulty, seed: Seed):
        """
        Add a map seed to the list of saved maps.
        """
        self.user_data['maps'][difficulty].add(seed)
    
    def replace_map(self, difficulty: GameDifficulty, seed: Seed):
        """
        Replaces the map seed data with the given map seed data.
        If the seed does not in the save data it will just be added.
        This would be used if you want to update the best time or if a map has been completed for example.
        """

        if seed in self.user_data['maps'][difficulty]:
            self.user_data['maps'][difficulty].remove(seed)
        self.add_map(difficulty, seed)
    
    def set_current_seed(self, difficulty: GameDifficulty, seed: Seed):
        """
        Set the current seed for a particular difficulty.
        """
        self.user_data['current_seed'][difficulty] = seed
    def get_current_seed(self, difficulty: GameDifficulty) -> Seed:
        """
        Get the current seed for a particular difficulty.
        """
        return self.user_data['current_seed'][difficulty]
    def get_user_name(self) -> str:
        """
        Get the user name from the save data.
        """
        return self.user_data['user_name']
    def set_user_name(self, user_name: str):
        """
        Set the user name in the save data.
        """
        self.user_data['user_name'] = user_name.strip()
