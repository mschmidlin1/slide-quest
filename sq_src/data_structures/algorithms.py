from sq_src.core.game_board import GameBoard
from sq_src.data_structures.game_enums import Direction, CellType
from sq_src.data_structures.data_types import Cell
import numpy as np
import copy
import collections

def ShortestPath(input_gameboard: GameBoard) -> list[Direction]:
    """
    This function takes in the gameboard and player position and will tell you
    the exact sequence of moves to complete the level in the minimum number of moves.

    If there is no possible path to the goal, and empty list is returned.

    This function deep copys the input gamebaord as to not manipulate it's state.

    This function uses Breadth First Search Algorithm (BFS).
    """

    gameboard = copy.deepcopy(input_gameboard)  # Use deepcopy if gameboard has nested objects
    queue = collections.deque()  # Use deque for efficient pops from the left
    queue.append((gameboard.player_pos, []))  # Start with the player position and an empty path
    goal_pos = gameboard.Find_Goal_Pos()
    visited = set()
    
    while queue:
        current_pos, path = queue.popleft()
        
        if current_pos == goal_pos:
            return path  # Return the path that led to the goal
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        
        for direction in Direction:
            gameboard.player_pos = current_pos
            next_pos = gameboard.MovePlayer(direction)
            
            # Check if next_pos is valid (not out of bounds or blocked)
            if next_pos!=current_pos and next_pos not in visited:
                # Append the current direction to the path and enqueue
                queue.append((next_pos, path + [direction]))
    
    return []  # Return an empty list if there's no path to the goal

def ReachablePositions(input_gameboard: GameBoard) -> set[Cell]:
    """
    This function takes in the gameboard and player position and returns a set of all
    reachable positions from the player's starting position.

    This function deep copys the input gameboard as to not manipulate it's state.

    This function uses Breadth First Search Algorithm (BFS).
    """

    gameboard = copy.deepcopy(input_gameboard)  # Use deepcopy if gameboard has nested objects
    queue = collections.deque()  # Use deque for efficient pops from the left
    start_pos = gameboard.player_pos
    queue.append(start_pos)  # Start with the player position
    visited = set()

    while queue:
        current_pos = queue.popleft()

        if current_pos in visited:
            continue

        visited.add(current_pos)

        for direction in Direction:
            gameboard.player_pos = current_pos
            next_pos = gameboard.MovePlayer(direction)

            # Check if next_pos is valid (not out of bounds or blocked)
            if next_pos != current_pos and next_pos not in visited:
                queue.append(next_pos)

    return visited

def FindConnectedBlocks(gameboard: GameBoard, start_cell: Cell) -> list[Cell]:
    """
    Finds all connected cells of the same type as the 'start_cell'.
    Uses Breadth-First Search (BFS) to explore the gameboard.

    Args:
    gameboard: An instance of GameBoard containing a .gameboard attribute which is a 2D numpy array.
    start_cell: A namedtuple 'Cell' indicating the starting position on the gameboard.

    Returns:
    list[Cell]: A list of all connected cells of the same type as 'start_cell'.
    """
    start_type = gameboard.Get_CellType(start_cell)
    # Directions for moving in the grid: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    connected_cells = []
    queue = collections.deque([start_cell])
    visited = set()
    visited.add(start_cell)
    
    while queue:
        current_cell = queue.popleft()
        connected_cells.append(current_cell)
        
        for direction in directions:
            next_row = current_cell.row + direction[0]
            next_col = current_cell.col + direction[1]
            next_cell = Cell(next_row, next_col)
            
            # Check if next_cell is within bounds and of the right type
            if (0 <= next_row < gameboard.gameboard.shape[0] and
                0 <= next_col < gameboard.gameboard.shape[1] and
                gameboard.gameboard[next_row, next_col] == start_type and
                next_cell not in visited):
                
                visited.add(next_cell)
                queue.append(next_cell)
    
    return connected_cells

def FindConnectedGroups(gameboard: GameBoard, cell_type: CellType = CellType.BLOCK) -> list[list[Cell]]:
    """
    Finds each connected group of cells of `cell_type` and returns each group in a set.
    """

    visited_cells = set()
    all_coordinates = [Cell(row, col) for row in range(gameboard.gameboard.shape[0]) for col in range(gameboard.gameboard.shape[1])]
    groups = []
    while len(all_coordinates)>0:
        current_coordinate = all_coordinates[0]
        if gameboard.Get_CellType(current_coordinate) != cell_type:
            all_coordinates.remove(current_coordinate)
            continue
        group = FindConnectedBlocks(gameboard, current_coordinate)
        groups.append(group)
        for coord in group:
            visited_cells.add(coord)
            all_coordinates.remove(coord)

    return groups

def DoesShapeFit(connected_cells: list[Cell], shape: tuple[int, int]) -> list[Cell]:
    """
    Determines if the shape fits into the connected cells.

    Args:
    connected_cells: The list of connected cells.
    shape: a tuple of the shape (rows, cols)  

    Returns:
    list[Cell]: A list of all the possible upper left corners that fit the desired shape. The list will be empty if the shape does not fit in the connected cells at all.
    """
    if len(connected_cells)==0:
        return []
    max_col = 0
    min_col = 1000
    max_row = 0
    min_row = 1000
    for cell in connected_cells:
        if cell.col > max_col:
            max_col = cell.col
        if cell.col < min_col:
            min_col = cell.col
        if cell.row > max_row:
            max_row = cell.row
        if cell.row < min_row:
            min_row = cell.row
    
    array = np.zeros((1+ max_row-min_row, 1+ max_col-min_col), dtype=int)

    for cell in connected_cells:
        array[cell.row-min_row, cell.col-min_col] = 1
    

    shape_array = np.ones(shape, dtype=int)
    shape_sum = np.sum(shape_array)

    possible_top_left_shape_corners = []

    for row_num, row in enumerate(array):
        for col_num, value in enumerate(row):
            if value != 1:
                continue
            if not ((row_num + shape[0]) <= array.shape[0]):
                continue
            if not ((col_num + shape[1]) <= array.shape[1]):
                continue

            sub_array = array[row_num:row_num + shape[0], col_num:col_num + shape[1]]
            product_array = sub_array*shape_array
            product_sum = np.sum(product_array)
            if shape_sum == product_sum:
                possible_top_left_shape_corners.append(Cell(row=row_num+min_row, col=col_num+min_col))

    return possible_top_left_shape_corners

def FindCoveredCells(loc: Cell, shape: tuple[int, int]) -> list[Cell]:
    """
    Computes and returns a list of Cells covered by a rectangular feature placed on the gameboard,
    excluding the top-left corner point. 

    Parameters:
    - loc (Cell): The top-left corner (x=row, y=column) of the feature on the gameboard.
    - shape: a tuple of the shape (rows, cols)

    Returns:
    list[Cell]: A list of Cells covered by the feature, excluding the initial top-left corner point.
    """
    nrows, ncols = shape
    points = []
    for row_num in range(loc.row, loc.row+nrows):
        for col_num in range(loc.col, loc.col+ncols):
            points.append(Cell(row_num, col_num))
    return points







