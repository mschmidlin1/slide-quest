from collections import namedtuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Point = namedtuple('Point', 'x y')#pixel coordinates
Cell = namedtuple("Cell", "row col")#goameboard positions
Size = namedtuple('Size', 'width height')
