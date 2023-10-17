from GameEnums import CellType, Direction
import numpy as np
from Point import Point

cell_dtype = np.dtype(CellType)
from modules.logging import set_logger, log

set_logger()

@log
class Grid:
    """
    A class that keeps track of the slide quest board and what cells are filled with what items. 
    """
    @log
    def __init__(self, grid_dims):
        """
        
        """
        self.grid_dims = grid_dims
        self.grid = np.empty(grid_dims, dtype=cell_dtype)
        self.grid.fill(CellType.EMPTY)
    @log
    def UpdateCell(self, location: Point, cell_type: CellType):
        """
        Adds a cell of type `type` to the coordinates `location` in the grid.
        """
        self.grid[location.x, location.y] = cell_type

    @log
    def NextBlock(self, direction: Direction):
        """
        Based on where the player is in the grid, it uses the `direction` and returns the type non empty block you encounter next.
        """
        if direction==Direction.DOWN:
            pass
        elif direction==Direction.LEFT:
            pass
        elif direction==Direction.RIGHT:
            pass
        elif direction==Direction.UP:
            pass

    # @log
    # def _next_