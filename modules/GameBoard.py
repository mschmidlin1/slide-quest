import sys
import os
#necessary to import things from the modules folder
sys.path.append(os.getcwd())

from modules.GameEnums import CellType, Direction
import numpy as np
from modules.Point import Point

cell_dtype = np.dtype(CellType)
from modules.my_logging import set_logger, log

set_logger()

@log
class GameBoard:
    """
    A class that keeps track of the slide quest board and what cells are filled with what `CellType`. 
    """
    @log
    def __init__(self, gameboard_dims):
        """
        
        """
        self.gameboard_dims = gameboard_dims
        self.gameboard = np.empty(gameboard_dims, dtype=cell_dtype)
        self.gameboard.fill(CellType.EMPTY)

        self.goal_pos = None
    @log
    def UpdateCell(self, location: Point, cell_type: CellType) -> None:
        """
        Adds a cell of type `type` to the coordinates `location` in the gameboard.
        """
        if cell_type==CellType.BORDER:
            raise ValueError("CellType.BORDER not settable on game board.")
        if cell_type==CellType.GOAL and self.goalPresent():
            raise ValueError("CellType.GOAL is already set on board.")
        self.gameboard[location] = cell_type
    @log
    def NextBlock(self, direction: Direction) -> (CellType, Point):
        """
        Based on where the player is in the gameboard, it uses the `direction` and returns the type of non empty block you encounter next.
        Returns (CellType, Point) where the type is the next type and Point is it's location.
        """
        if not self.isGameBoardReady():
            raise ValueError("GameBoard play board is not set up.")

        self.player_position = self.Find_Player_Pos()

        if direction==Direction.DOWN:
            #get column player is in
            col = self.gameboard[:,self.player_position.x]
            #get the index in the column (moving downward) that has the next non empty cell
            cell_type, idx = self._next_occupied_cell(col, self.player_position.y+1)
            next_cell_pos = Point(self.player_position.x, idx)
            return cell_type, next_cell_pos
        elif direction==Direction.UP:
            #get column player is in, the [::-1] reverses the direction of the array
            col = self.gameboard[:,self.player_position.x][::-1]
            #get the index in the column (moving upward) that has the next non empty cell, the len(col) - pos is to reverse the position in the array 
            cell_type, idx = self._next_occupied_cell(col, len(col) - self.player_position.y+1)
            next_cell_pos = Point(self.player_position.x, len(col) - idx)
            return cell_type, next_cell_pos
        elif direction==Direction.RIGHT:
            #get row the player is in
            row = self.gameboard[self.player_position.y,:]
            #get the index in the row (moving right) that has the next non empty cell
            cell_type, idx = self._next_occupied_cell(row, self.player_position.x+1)
            next_cell_pos = Point(idx, self.player_position.y)
            return cell_type, next_cell_pos
        elif direction==Direction.LEFT:
            #get row the player is in, the [::-1] reverses the direction of the array
            row = self.gameboard[self.player_position.y,:][::-1]
            #get the index in the row (moving right) that has the next non empty cell, the len(row) - pos is to reverse the position in the array 
            cell_type, idx = self._next_occupied_cell(row, len(row) - self.player_position.x+1)
            next_cell_pos = Point(len(row) - idx, self.player_position.y)
            return cell_type, next_cell_pos
        else:
            raise NotImplementedError(f"Direction type {direction} not implemented.")
    @log
    def _next_occupied_cell(self, array, start: int) -> (CellType, int):
        """
        Takes in an array and iterates through the array until the next non empty cell.

        Starts at the index `start`. This should generally refer to the player location+1. 

        Returns (`CellType`, `int`) where the int is the index of the next non empty cell.

        If all cells are emtpy `(CellType.BORDER, len(array))` is returned.
        """
        for i in range(start, len(array)):
            cell = array[i]
            if cell!=CellType.EMPTY:
                return cell, i
        return CellType.BORDER, len(array)
    @log
    def isGameBoardReady(self) -> bool:
        """
        Checks if there is a player and at least one blocker in the GameBoard.
        """
        return self.playerPresent() and self.blockerPresent() and self.goalPresent()
    @log
    def playerPresent(self) -> bool:
        """
        Checks if the player position is set somewhere in the GameBoard.
        """
        return np.sum(np.isin(self.gameboard, [CellType.PLAYER])) > 0
    @log
    def blockerPresent(self) -> bool:
        """
        Checks if at least one blocker is set somewhere in the GameBoard.
        """
        return np.sum(np.isin(self.gameboard, [CellType.BLOCKED])) > 0
    @log
    def goalPresent(self) -> bool:
        """
        Checks if the goal is set somewhere in the GameBoard.
        """
        return np.sum(np.isin(self.gameboard, [CellType.GOAL])) > 0
    @log
    def Find_Player_Pos(self) -> Point:
        """
        Finds the player position in the GameBoard.
        """
        return Point(*np.where(self.gameboard==CellType.PLAYER)[0])
    @log
    def Find_Goal_Pos(self) -> Point:
        """
        Finds the goal position in the GameBoard.
        """
        return Point(*np.where(self.gameboard==CellType.GOAL)[0])
    @log
    def MovePlayer(self, direction: Direction) -> Point:
        """
        Returns the new location of the player.
        Also updates the gameboard with the new player location.
        """
        cell_type, location = self.NextBlock(direction)

        if cell_type==CellType.BLOCKED or cell_type==CellType.BORDER:
            if direction == Direction.DOWN:
                new_player_pos = Point(location.x, location.y-1)
            elif direction == Direction.UP:
                new_player_pos = Point(location.x, location.y+1)
            elif direction == Direction.RIGHT:
                new_player_pos = Point(location.x-1, location.y)
            elif direction == Direction.LEFT:
                new_player_pos = Point(location.x+1, location.y)
            else:
                raise NotImplementedError(f"Direction type {direction} not implemented.")
            self.UpdateCell(self.Find_Player_Pos(), CellType.EMPTY)
            self.UpdateCell(new_player_pos, CellType.PLAYER)
            return new_player_pos
        
        elif cell_type==CellType.GOAL:
            self.UpdateCell(self.Find_Player_Pos(), CellType.EMPTY)
            self.UpdateCell(location, CellType.PLAYER)
            return location 
        else:
            raise NotImplementedError(f"Cell type of {cell_type} not implemented for 'MovePlayer' method.")