from sq_src.data_structures.game_enums import Direction


class Seed:
    """
    Represents a game seed with its associated path, completion status, and performance metrics.

    Attributes:
        seed (int): The identifier for the game seed.
        shortest_path (list[Direction]): A list of directions representing the shortest path to complete the game.
        completed (bool): A flag indicating whether the game has been completed using this seed.
        best_time_ms (float): The best time recorded for completing the game with this seed, in milliseconds.
        best_num_moves (int): The smallest number of moves taken to complete the game with this seed.
        stars (int): The number of stars earned for this level (0-3).

    Methods:
        __init__(self, seed, shortest_path, completed, best_time_ms, best_num_moves, stars): Initializes a new Seed instance.
        __eq__(self, other): Checks equality based on the seed attribute.
        __hash__(self): Returns the hash based on the seed attribute.
    """
    number: int
    shortest_path: list[Direction]
    completed: bool
    is_possible: bool
    best_time_ms: float
    best_num_moves: int
    stars: int

    def __init__(self, seed: int, shortest_path: list[Direction], completed: bool, is_possible: bool, best_time_ms: float, best_num_moves: int, stars: int = 0):
        """
        Constructs a Seed instance with the provided seed identifier, path, completion status, best time, and number of moves.

        Parameters:
            seed (int): The identifier for the game seed.
            shortest_path (list[Direction]): A list of directions representing the shortest path to complete the game.
            completed (bool): Indicates whether the game has been completed using this seed.
            is_possible (bool): Indicates whether the map is possible to solve.
            best_time_ms (float): The best time recorded for completing the game with this seed, in milliseconds.
            best_num_moves (int): The smallest number of moves taken to complete the game with this seed.
            stars (int): The number of stars earned for this level (0-3). Defaults to 0.
        """
        self.number = seed
        self.shortest_path = shortest_path
        self.completed = completed
        self.is_possible = is_possible
        self.best_time_ms = best_time_ms
        self.best_num_moves = best_num_moves
        self.stars = stars

    def __eq__(self, other):
        """
        Checks if another object is equal to this Seed instance based on the seed identifier.

        Parameters:
            other (any): The object to compare.

        Returns:
            bool: True if other is a Seed instance with the same seed identifier, False otherwise.
        """
        if isinstance(other, Seed):
            return self.number == other.number
        return False

    def __hash__(self):
        """
        Returns the hash based on the seed attribute. This makes the object usable in sets and as dictionary keys.

        Returns:
            int: The hash value of the seed attribute.
        """
        return hash(self.number)
    
    def __str__(self) -> str:
        return f"Seed(Number: {self.number}   Completed: {self.completed}   Is_Possible: {self.is_possible}   Stars: {self.stars})"

