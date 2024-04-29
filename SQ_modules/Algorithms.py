from SQ_modules.GameBoard import GameBoard
from SQ_modules.GameEnums import Direction, CellType
from SQ_modules.DataTypes import Cell
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


