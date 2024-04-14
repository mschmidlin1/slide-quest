from SQ_modules.Metas import SingletonMeta
import os
from SQ_modules.configs import GAME_VOLUME
from SQ_modules.GameEnums import GameDifficulty
import pickle
from SQ_modules.my_logging import set_logger
import logging
set_logger()


class UserData(metaclass=SingletonMeta):
    """
    A singleton class for managing user data in a game.

    Attributes:
        file_name (str): The name of the file where user data is saved.
        music_volume (float): The music volume level.
        sfx_volume (float): The sound effects volume level.
        completed_seeds (Dict[GameDifficulty, Set[int]]): A dictionary tracking completed levels, categorized by difficulty.
        user_data (dict): A dictionary containing all user data including volume levels and completed maps.

    Methods:
        write(): Save the user_data dictionary to a file.
        read(): Load the user_data dictionary from a file.
        update_music_volume(volume): Set the music volume and save the change.
        update_sfx_volume(volume): Set the sound effects volume and save the change.
        add_completed_level(difficulty, seed): Mark a level as completed and save the change.
    """
    file_name: str = "save_data.pkl"
    music_volume: float
    sfx_volume: float
    completed_seeds: dict[GameDifficulty, set[int]]
    user_data: dict
    def __init__(self):
        """Initialize the UserData object, loading existing data from file or creating new default values."""

        self.completed_seeds = {difficulty: set() for difficulty in GameDifficulty}
        self.music_volume = GAME_VOLUME
        self.sfx_volume = GAME_VOLUME


        if not os.path.exists(self.file_name):
            self.user_data = {
                    "volume_levels": {
                        "music": self.music_volume,
                        "sfx": self.sfx_volume
                    },
                    "completed_maps": self.completed_seeds
                }
            self.write()
        else:
            self.read()
    

    def write(self):
        """Save the current state of user_data to a file."""
        try:
            with open(self.file_name, 'wb') as f:
                pickle.dump(self.user_data, f)
        except IOError as e:
            logging.info(f"Error writing to file: {e}")

    def read(self):
        """Load user data from the file."""
        try:
            with open(self.file_name, 'rb') as f:
                loaded_data = pickle.load(f)
                self.user_data = loaded_data
        except (IOError, EOFError, pickle.UnpicklingError) as e:
            logging.info(f"Error reading from file: {e}")
    
    def update_music_volume(self, volume: float):
        """Update the music volume level in the user data and write to file."""
        self.user_data['volume_levels']['music'] = volume
        self.write()

    def update_sfx_volume(self, volume: float):
        """Update the sound effects volume level in the user data and write to file."""
        self.user_data['volume_levels']['sfx'] = volume
        self.write()

    def add_completed_level(self, difficulty: GameDifficulty, seed: int):
        """Record a completed level by difficulty and seed in the user data and write to file."""
        self.user_data['completed_maps'][difficulty].add(seed)
        self.write()
