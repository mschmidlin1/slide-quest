from datetime import datetime
import sys
import os
import re

#necessary to import things from the modules folder
sys.path.append(os.getcwd())
from modules.GameBoard import GameBoard
from modules.my_logging import set_logger, log
from modules.GameEnums import CellType, Str_to_CellType_vector_func, GameDifficulty, Game_Difficult_Str_Map
from modules.DataTypes import Point
import numpy as np
cell_dtype = np.dtype(CellType)
set_logger()


class LevelIO:
    """
    Class for managing levels and completed levels in a SlideQuest.

    Attributes:
    -----------
        `.current_level` (str): The current level being played.

    Methods:
    --------
        `get_player_file() -> str`: Returns the associated player position file name for the current level.

        `next_level() -> None`: Moves to the next level, marking the current level as completed
            and updating the current level attribute.
    """
    def __init__(self):
        self.levels_root_dir = "levels"
        self.completed_levels_file = "levels/#_completed.txt" 

        self.level_file_pattern = r'^(\d_\d{4}-\d{2}-\d{2} \d{2}\.\d{2}\.\d{2}\.\d{6}\.csv)$'

        self.all_levels = self.list_levels(self.levels_root_dir)
        self.completed_levels = self.read_completed(self.completed_levels_file)
        self.incomplete_levels = self.filter_by_completed(self.all_levels, self.completed_levels)
        if len(self.incomplete_levels)<1:
            self.clear_completed()

        self.current_level = self.incomplete_levels.pop(0)
        
        self.current_difficulty: GameDifficulty = Game_Difficult_Str_Map[os.path.basename(self.current_level)[0]]

    @log
    def check_completed_file(self) -> None:
        """
        Checks if the completed file is is there and creates a blank one if not.
        """
        if not os.path.exists(self.completed_levels_file):
            with open(self.completed_levels_file, "w") as file:
                pass
    @log
    def list_levels(self, path: str) -> list[str]:
        """
        This method does an intelligent regex search of a directory and returns all the "map" type files.
        """
        all_files = os.listdir(path)
        match_func = lambda s: re.match(self.level_file_pattern, s)
        level_files = list(filter(match_func, all_files))
        level_paths = [os.path.join(path, f) for f in level_files]
        return level_paths
    @log
    def filter_by_completed(self, all_levels: list[str], completed_levels: list[str]) -> list[str]:
        """
        This method takes in a list of all the levels in existence and filters them by which have been completed.
        """
        filter_func = lambda l: l not in completed_levels
        incomplete_levels = list(filter(filter_func, all_levels))
        return incomplete_levels
    @log
    def read_completed(self, file_path: str) -> list[str]:
        """
        This method takes in a file path of the type that houses a list of completed levels and returns the levels in a list of strings.
        """
        with open(file_path, 'r') as file:
            lines = []
            for line in file:
                line = line.strip()
                lines.append(line)
        return lines
    @log
    def get_player_file(self) -> str:
        """
        Using the `.current_level` this method finds the associated player position file and returns the file name.
        """
        map_str = self.current_level[:-4]
        return map_str + '-player.txt'
    @log
    def append_completed_to_file(self, level_name: str) -> None:
        """
        Takes in a level name file and adds it to the appropriate level completed file.
        """
        with open(self.completed_levels_file, "a") as f:
            f.write(f"{level_name}\n")
    @log
    def next_level(self) -> None:
        """
        Adds the current level to the list of completed levels. 
        Gets the new level and assigns it to `.current_level`
        """
        self.completed_levels.append(self.current_level)
        self.append_completed_to_file(self.current_level)
        if len(self.incomplete_levels)<1:
            self.clear_completed()
        self.current_level = self.incomplete_levels.pop(0)
        self.current_difficulty: GameDifficulty = Game_Difficult_Str_Map[os.path.basename(self.current_level)[0]]
    @log    
    def clear_completed(self) -> None:
        """
        Overwrites completed level list with a blank one an re-initializes internal completion tracking.
        """
        with open(self.completed_levels_file, "w") as file:
            pass
        self.all_levels = self.list_levels(self.levels_root_dir)
        self.completed_levels = self.read_completed(self.completed_levels_file)
        self.incomplete_levels = self.filter_by_completed(self.all_levels, self.completed_levels)
    @log
    def SaveBoard(self, gameboard: GameBoard, filename: str) -> None:
        """
        Saves the current state of the gameboard to a csv file using the current dttm LevelIO save format.
        """
        with open(filename, mode='w', newline='') as file:
            file.write(str(gameboard))
    @log
    def SavePlayerPos(self, pos: Point, filename: str) -> None:
        """
        Saves the player position to a file using the current dttm LevelIO save format.
        """
        pos_str = f"({pos.x},{pos.y})"
        with open(filename, mode='w', newline='') as file:
            file.write(pos_str)
    @log
    def SaveNew(self, gameboard: GameBoard) -> None:
        """
        Saves the board and the player pos to an new level file.
        """
        level_str = os.path.basename(self.current_level)[0] + '_'
        str_dttm = self.str_dttm()
        player_file = level_str + str_dttm + "-player.txt"
        map_file = level_str + str_dttm + ".csv"
        player_file = os.path.join(self.levels_root_dir, player_file)
        map_file = os.path.join(self.levels_root_dir, map_file)
        self.SavePlayerPos(gameboard.player_pos, player_file)
        self.SaveBoard(gameboard, map_file)
    @log
    def SaveInPlace(self, gameboard: GameBoard) -> None:
        """
        Overwrite the map you are currently on.
        """
        self.SavePlayerPos(gameboard.player_pos, self.get_player_file())
        self.SaveBoard(gameboard, self.current_level)
    @log
    def ReadBoard(self, filename: str = None) -> np.ndarray:
        """
        Reads the celltypes from a file and loads them into a numpy array.
        Will use the self.current_level unless `filename` is passed.
        """
        if filename is None:
            filename = self.current_level
        with open(filename, mode='r', newline='') as f:
            all_lines = f.readlines()

        string_cells = []
        for line in all_lines:
            line = line.strip()
            string_cells.append(line.split(','))
        string_cells = np.array(string_cells)
        gameboard = Str_to_CellType_vector_func(string_cells)
        gameboard = gameboard.astype(cell_dtype)

        return gameboard
    @log
    def ReadPlayerPos(self, filename: str = None) -> Point:
        """
        Reads the player position from a file.
        Will use the self.current_level unless `filename` is passed.
        """
        if filename is None:
            filename = self.get_player_file()
        with open(filename, mode='r', newline='') as f:
            all_lines = f.readlines()
        pos_str = all_lines[0].strip()
        pos_str = pos_str.replace("(", "")
        pos_str = pos_str.replace(")", "")
        x, y = pos_str.split(",")
        x = x.strip()
        y = y.strip()
        return Point(int(x), int(y))
    @log
    def Read(self) -> tuple[np.ndarray, Point]:
        gameboard = self.ReadBoard(self.current_level)
        player_pos = self.ReadPlayerPos(self.get_player_file())
        return gameboard, player_pos
    @log
    def str_dttm(self) -> str:
        """
        This method gets the current datetime string and returns it.
        """
        return datetime.now().__str__().replace(":",".")
