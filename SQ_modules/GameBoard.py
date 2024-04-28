import sys
import os
#necessary to import things from the SQ_modules folder
sys.path.append(os.getcwd())

from SQ_modules.GameEnums import CellType, Direction, Str_to_CellType_vector_func
from SQ_modules.configs import Difficulty_Lookup
import numpy as np
from SQ_modules.DataTypes import Cell, Size
from SQ_modules.GameEnums import GameDifficulty
cell_dtype = np.dtype(CellType)
from SQ_modules.my_logging import set_logger, log

set_logger()


class GameBoard:
    """
    A class that keeps track of the slide quest board and what cells are filled with what `CellType`. 
    """
    
    def __init__(self, gameboard: np.ndarray, player_pos: Cell):
        """
        
        """
        self.gameboard = gameboard
        self.goal_pos: Cell = self.Find_Goal_Pos()
        self.player_pos: Cell = player_pos
        self.difficulty: GameDifficulty = Difficulty_Lookup[Size(gameboard.shape[1], gameboard.shape[0])]
    
    def UpdateCell(self, location: Cell, cell_type: CellType) -> None:
        """
        Adds a cell of type `type` to the coordinates `location` in the gameboard.

        Will override the cell if it is already occupied.
        """
        #see if cell is occupied
        if location == self.player_pos and (cell_type not in [CellType.ICE, CellType.GROUND]):
            raise ValueError(f"{cell_type} and player cannot share a cell.")
        if cell_type==CellType.BORDER:
            raise ValueError("CellType.BORDER not settable on game board.")
        if cell_type==CellType.GOAL and self.goalPresent():
            raise ValueError("CellType.GOAL is already set on board.")
        if cell_type==CellType.GOAL:
            self.goal_pos = location
        if cell_type==CellType.PLAYER:
            raise ValueError("Incorrect use of update cell. Use `SetPlayerPos()` method.")
        self.gameboard[location.row, location.col] = cell_type
    
    def SetPlayerPos(self, location: Cell) -> None:
        """
        Sets the player position to be controlled by the Gameboard.
        """
        if self.gameboard[location.row, location.col] not in [CellType.ICE, CellType.GROUND]:
            raise ValueError(f"{location} is already filled with {self.gameboard[location.row, location.col]}")
        self.player_pos = location
    
    def GetPlayerPos(self) -> Cell:
        """
        Gets the Player position.
        """
        if self.player_pos == None:
            raise RuntimeError("Player position hasn't been set yet!")
        return self.player_pos
    
    def NextBlock(self, direction: Direction) -> tuple[CellType, Cell]:
        """
        Based on where the player is in the gameboard, it uses the `direction` and returns the type of non ice block you encounter next.
        Returns (CellType, Cell) where the type is the next type and Cell is it's location.
        """
        if not self.isGameBoardReady():
            raise ValueError("GameBoard play board is not set up.")

        if direction==Direction.DOWN:
            #get column player is in
            col = self.gameboard[:,self.player_pos.col]
            #get the index in the column (moving downward) that has the next non empty cell
            cell_type, idx = self._next_occupied_cell(col, self.player_pos.row+1)
            next_cell_pos = Cell(idx, self.player_pos.col)
            return cell_type, next_cell_pos
        elif direction==Direction.UP:
            #get column player is in, the [::-1] reverses the direction of the array
            col = self.gameboard[:,self.player_pos.col][::-1]
            #get the index in the column (moving upward) that has the next non empty cell, the len(col) - pos is to reverse the position in the array 
            cell_type, idx = self._next_occupied_cell(col, len(col) - self.player_pos.row)
            next_cell_pos = Cell(len(col) - idx-1, self.player_pos.col)
            return cell_type, next_cell_pos
        elif direction==Direction.RIGHT:
            #get row the player is in
            row = self.gameboard[self.player_pos.row,:]
            #get the index in the row (moving right) that has the next non empty cell
            cell_type, idx = self._next_occupied_cell(row, self.player_pos.col+1)
            next_cell_pos = Cell(self.player_pos.row, idx)
            return cell_type, next_cell_pos
        elif direction==Direction.LEFT:
            #get row the player is in, the [::-1] reverses the direction of the array
            row = self.gameboard[self.player_pos.row,:][::-1]
            #get the index in the row (moving right) that has the next non empty cell, the len(row) - pos is to reverse the position in the array 
            cell_type, idx = self._next_occupied_cell(row, len(row) - self.player_pos.col)
            next_cell_pos = Cell(self.player_pos.row, len(row) - idx-1)
            return cell_type, next_cell_pos
        else:
            raise NotImplementedError(f"Direction type {direction} not implemented.")
    
    def _next_occupied_cell(self, array, start: int) -> tuple[CellType, int]:
        """
        Takes in an array and iterates through the array until the next non ice cell.

        Starts at the index `start`. This should generally refer to the player location+1. 

        Returns (`CellType`, `int`) where the int is the index of the next non ice cell.

        If all cells are emtpy `(CellType.BORDER, len(array))` is returned.
        """
        for i in range(start, len(array)):
            cell = array[i]
            if cell!=CellType.ICE:
                return cell, i
        return CellType.BORDER, len(array)
    
    def isGameBoardReady(self) -> bool:
        """
        Checks if there is a player and at least one blocker in the GameBoard.
        """
        return self.playerPresent() and self.blockerPresent() and self.goalPresent()
    
    def playerPresent(self) -> bool:
        """
        Checks if the player position has been set.
        """
        return self.player_pos!=None
    
    def blockerPresent(self) -> bool:
        """
        Checks if at least one blocker is set somewhere in the GameBoard.
        """
        return np.sum(np.isin(self.gameboard, [CellType.BLOCK])) > 0
    
    def goalPresent(self) -> bool:
        """
        Checks if the goal is set somewhere in the GameBoard.
        """
        return np.sum(np.isin(self.gameboard, [CellType.GOAL])) > 0
    
    def Find_Goal_Pos(self) -> Cell:
        """
        Finds the goal position in the GameBoard.
        """
        if not self.goalPresent():
            raise ValueError(f"Goal not on board yet.")
        row_indexs, col_indexs = np.where(self.gameboard==CellType.GOAL)
        if row_indexs.__len__()>1 or col_indexs.__len__()>1:
            raise ValueError(f"More than one location found for CellType.GOAL.")
        return Cell(row_indexs[0], col_indexs[0])
    
    def MovePlayer(self, direction: Direction) -> Cell:
        """
        Returns the new location of the player.
        Also updates the gameboard with the new player location.
        """
        cell_type, location = self.NextBlock(direction)

        if cell_type==CellType.BLOCK or cell_type==CellType.BORDER:
            if direction == Direction.DOWN:
                new_player_pos = Cell(location.row-1, location.col)
            elif direction == Direction.UP:
                new_player_pos = Cell(location.row+1, location.col)
            elif direction == Direction.RIGHT:
                new_player_pos = Cell(location.row, location.col-1)
            elif direction == Direction.LEFT:
                new_player_pos = Cell(location.row, location.col+1)
            else:
                raise NotImplementedError(f"Direction type {direction} not implemented.")
            self.player_pos = new_player_pos
            return new_player_pos
        
        elif cell_type==CellType.GOAL or cell_type==CellType.GROUND:
            self.player_pos = location
            return location
        else:
            raise NotImplementedError(f"Cell type of {cell_type} not implemented for 'MovePlayer' method.")
    
    def __str__(self) -> str:
        """
        Returns the GameBaord as a string with each row separated by '\\n' and each cell separated by ','.
        """
        return '\n'.join([','.join(list(map(str, row))) for row in self.gameboard])
    
    def Get_CellType(self, loc: Cell) -> CellType:
        """
        Given a location on the gameboard, gets the CellType that occupies that location.
        """
        return self.gameboard[loc.row, loc.col]
    def Crop(self, upper_left: Cell, lower_right: Cell) -> np.ndarray:
        """
        Crops the provided rectangle from the gameboard and returns the sub-array. The lower right corner WILL be included in the returned array. 
        """
        return self.gameboard[upper_left.row:lower_right.row+1,upper_left.col:lower_right.col+1]

    def __eq__(self, other) -> bool:
        if np.array_equal(self.gameboard, other.gameboard) and self.player_pos==other.player_pos and self.goal_pos==other.goal_pos:
            return True
        else:
            return False


if __name__=="__main__":
    # my_gameboard = GameBoard((10, 10))
    # my_gameboard.SaveBoard("test.csv")
    # my_gameboard.ReadBoard("test.csv")
    my_gameboard = GameBoard((26, 26))
    my_gameboard.ReadBoard("test copy.csv")
    # print(my_gameboard)