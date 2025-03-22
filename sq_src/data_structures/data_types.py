from collections import namedtuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Point = namedtuple('Point', 'x y')#pixel coordinates
Cell = namedtuple("Cell", "row col")#goameboard positions
Size = namedtuple('Size', 'width height')

from enum import Enum

class Anchor(Enum):
    """Enum for specifying the anchor point of a notification banner."""
    TOP_LEFT = "topleft"
    TOP_RIGHT = "topright"
    BOTTOM_LEFT = "bottomleft"
    BOTTOM_RIGHT = "bottomright"
    CENTER = "center"
