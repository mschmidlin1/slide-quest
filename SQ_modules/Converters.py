from SQ_modules.DataTypes import Cell, Point
from SQ_modules.GameEnums import CellType, GameDifficulty
from SQ_modules.configs import CELL_DIMENSIONS, Border_Size_Lookup, WINDOW_DIMENSIONS, Board_Size_Lookup


def CellToPoint(cell: Cell, difficulty: GameDifficulty) -> Point:
    """
    Converts a `Cell` object, representing a cell's row and column coordinates on the game board,
    into a `Point` object, which represents the corresponding x and y pixel coordinates on the screen.

    Important Notes:
    ----------
    Returns the point in the middle of the Cell.\n
    Rounds to the nearest whole pixel value. Will not return a decimal.

    Parameters:
    -----------
    - `cell` (Cell): An object representing the cell's location on the game board, containing `row` and `column` attributes.
    - `difficulty` (GameDifficulty): An enumeration value or similar representation indicating the game's difficulty level.
      This affects the border size around the game board, which in turn influences the calculation of pixel coordinates.

    Returns:
    --------
    - Point : An object representing the calculated x and y pixel coordinates corresponding to the center of the specified cell.

    Example:
    --------
    ```
    cell = Cell(row=3, col=5)
    difficulty = GameDifficulty.EASY
    pixel_point = CellToPoint(cell, difficulty)

    print(f"Pixel coordinates: {pixel_point.x}, {pixel_point.y}")
    ```
    """
    if cell.row<0 or cell.col<0:
        raise ValueError(f"cell.row and cell.col cannot be negative.")

    if cell.row > Board_Size_Lookup[difficulty].height - 1:
        raise ValueError(f"cell.row is outside the bounds for {difficulty} difficulty.")
    
    if cell.col > Board_Size_Lookup[difficulty].width - 1:
        raise ValueError(f"cell.col is outside the bounds for {difficulty} difficulty.")

    x = Border_Size_Lookup[difficulty].width + (cell.col * CELL_DIMENSIONS.width) + (CELL_DIMENSIONS.width // 2)
    y = Border_Size_Lookup[difficulty].width + (cell.row * CELL_DIMENSIONS.height) + (CELL_DIMENSIONS.height // 2)
    return Point(round(x), round(y))

def PointToCell(point: Point, difficulty: GameDifficulty) -> Cell:
    """
    Converts a `Point` object, representing x and y pixel coordinates on the screen,
    to a `Cell` object, which represents the cell's row and column coordinates on the game board.

    Important Notes:
    ----------
    If the Point is outside the bounds of the gameboard. None is returned.

    Parameters:
    -----------
    - `point` (Point): An object representing the x and y pixel coordinates on the screen.
    - `difficulty` (GameDifficulty): An enumeration value or similar representation indicating the game's difficulty level.
      This affects the border size around the game board, which in turn influences the calculation of cell coordinates.

    Returns:
    --------
    - Cell: An object representing the row and column of the game board that corresponds to the given pixel coordinates.
        If the Point is outside the bounds of the gameboard. None is returned.

    Example:
    --------
    ```
    point = Point(x=150, y=200)
    difficulty = GameDifficulty.EASY
    game_cell = PointToCell(point, difficulty)

    print(f"Game board cell: Row {game_cell.row}, Column {game_cell.col}")
    ```
    """
    if point.x<Border_Size_Lookup[difficulty].width: #check if point is in left border
        return None
    if point.y<Border_Size_Lookup[difficulty].height: #check if point is in top border
        return None
    if point.x>(WINDOW_DIMENSIONS.width-Border_Size_Lookup[difficulty].width): #check if point is in right border
        return None
    if point.y>(WINDOW_DIMENSIONS.height-Border_Size_Lookup[difficulty].height): #check if point is in bottom border
        return None
    
    col = (point.x - Border_Size_Lookup[difficulty].width) // CELL_DIMENSIONS.width
    row = (point.y - Border_Size_Lookup[difficulty].height) // CELL_DIMENSIONS.height

    return Cell(row=int(row), col=int(col))

