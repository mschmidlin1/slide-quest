from SQ_modules.GameBoard import GameBoard
from SQ_modules.GameEnums import Direction
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
