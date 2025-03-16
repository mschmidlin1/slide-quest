




from sq_src.data_structures.game_enums import CellType


class Neighbors:
    """
    A container class to hold the CellType values of all neighboring cells.

    Attributes:
        top (CellType): The CellType of the cell directly above.
        bottom (CellType): The CellType of the cell directly below.
        left (CellType): The CellType of the cell directly to the left.
        right (CellType): The CellType of the cell directly to the right.
        top_left (CellType): The CellType of the cell diagonally above and to the left.
        top_right (CellType): The CellType of the cell diagonally above and to the right.
        bottom_left (CellType): The CellType of the cell diagonally below and to the left.
        bottom_right (CellType): The CellType of the cell diagonally below and to the right.
    """

    def __init__(self, top: CellType, bottom: CellType, left: CellType, right: CellType,
                 top_left: CellType, top_right: CellType, bottom_left: CellType, bottom_right: CellType):
        """
        Initializes a Neighbors object with the CellType values of all neighbors.

        Args:
            top (CellType): The CellType of the cell directly above.
            bottom (CellType): The CellType of the cell directly below.
            left (CellType): The CellType of the cell directly to the left.
            right (CellType): The CellType of the cell directly to the right.
            top_left (CellType): The CellType of the cell diagonally above and to the left.
            top_right (CellType): The CellType of the cell diagonally above and to the right.
            bottom_left (CellType): The CellType of the cell diagonally below and to the left.
            bottom_right (CellType): The CellType of the cell diagonally below and to the right.
        """
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right