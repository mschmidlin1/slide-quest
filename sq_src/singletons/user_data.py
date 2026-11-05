from sq_src.level_generation.seed import Seed
from sq_src.metas import SingletonMeta
import base64
import os
import pickle
import sys
from sq_src.configs import GAME_VOLUME
from sq_src.data_structures.game_enums import GameDifficulty, Direction
from sq_src.singletons.my_logging import LoggingService

BROWSER_SAVE_KEY = "slidequest.save_data"





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
        self.logging_service = LoggingService()


        if os.path.exists(self.file_name):
            self.read()
        if not hasattr(self, "user_data"):
            if not self._read_browser():
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
    

    def write(self):
        """
        Saves the user data to file.
        """
        payload = pickle.dumps(self.user_data)
        try:
            with open(self.file_name, 'wb') as f:
                f.write(payload)
        except IOError as e:
            self.logging_service.log_error(f"Error writing to file: {e}")
        self._write_browser(payload)

    def read(self):
        """
        Loads the user data from file.
        """
        try:
            with open(self.file_name, 'rb') as f:
                loaded_data = pickle.load(f)
                self.user_data = loaded_data
        except (IOError, EOFError, pickle.UnpicklingError) as e:
            self.logging_service.log_error(f"Error reading from file: {e}")

    def _browser_storage(self):
        """Return the browser localStorage object when running under pygbag."""
        if sys.platform != "emscripten":
            return None
        try:
            from platform import window
            return window.localStorage
        except Exception:
            return None

    def _write_browser(self, payload: bytes):
        storage = self._browser_storage()
        if storage is None:
            return
        try:
            storage.setItem(BROWSER_SAVE_KEY, base64.b64encode(payload).decode("ascii"))
        except Exception as e:
            self.logging_service.log_error(f"Error writing browser save: {e}")

    def _read_browser(self) -> bool:
        storage = self._browser_storage()
        if storage is None:
            return False
        try:
            raw = storage.getItem(BROWSER_SAVE_KEY)
            if not raw:
                return False
            self.user_data = pickle.loads(base64.b64decode(str(raw)))
            return True
        except Exception as e:
            self.logging_service.log_error(f"Error reading browser save: {e}")
            return False
    
    def update_music_volume(self, volume: float):
        """
        Update the saved music volume.
        """
        self.user_data['volume_levels']['music'] = volume
        self.write()

    def update_sfx_volume(self, volume: float):
        """
        Update the saved sound effects volume.
        """
        self.user_data['volume_levels']['sfx'] = volume
        self.write()

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
        self.write()

    def get_seeds(self, difficulty: GameDifficulty) -> list[Seed]:
        """
        Get a list of Seed objects for the specified difficulty.
        """
        return list(self.user_data['maps'][difficulty])
