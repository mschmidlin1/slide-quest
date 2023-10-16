import numpy as np
from enum import Enum

class CellType(Enum):
    EMPTY = 1
    BLOCKED = 2
    PLAYER = 3
    PORTAL = 4
    POWER_UP = 5


Cell_dtype = np.dtype(CellType)
arr = np.empty((10, 10), dtype=Cell_dtype)
arr.fill(CellType.EMPTY)