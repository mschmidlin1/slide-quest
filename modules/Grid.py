from GameEnums import CellType
import numpy as np
from Point import Point

cell_dtype = np.dtype(CellType)

class Grid:
    """
    A class that keeps track of the slide quest board and what cells are filled with what items. 
    """
    def __init__(self, grid_dims, ):
        """
        
        """
        self.grid_dims = grid_dims
        self.grid = np.empty(grid_dims, dtype=cell_dtype)
        self.grid.fill(CellType.EMPTY)

    def AddCellType(self, location: Point, type: CellType):
        """
        Adds a cell of type `type` to the coordinates `location` in the grid.
        """
        


