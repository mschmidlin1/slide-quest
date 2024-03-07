import pygame
from pygame.sprite import Sprite
from SQ_modules.DataTypes import Cell
from SQ_modules.GameEnums import CellType
from SQ_modules.GameBoard import GameBoard
import numpy as np
from SQ_modules.Sprites import Player, Goal, Block, Ice
sprite_dtype = np.dtype(Sprite)



def CellType_To_Sprite(cell_type: CellType) -> Sprite:
    """
    Takes a cell type and returns it's type of sprite.

    This method does not return a Sprite object, it returns a Sprite type. A reference to the class.
    """
    if cell_type == CellType.PLAYER:
        return Player
    elif cell_type == CellType.GOAL:
        return Goal
    elif cell_type == CellType.BLOCK:
        return Block
    elif cell_type == CellType.ICE:
        return Ice
    else:
        raise NotImplementedError(f"CellType_To_Sprite() not implemented for {cell_type}")
    
def Sprite_To_CellType(sprite: Sprite) -> CellType:
    """
    Takes a Sprite and returns it's CellType.

    Note, this method takes a type. For example Player, Goal, etc...

    It does not take an object of type Sprite.
    """
    if sprite == Player:
        return CellType.PLAYER
    elif sprite == Goal:
        return CellType.GOAL
    elif sprite == Block:
        return CellType.BLOCK
    elif sprite == Ice:
        return CellType.ICE
    else:
        raise NotImplementedError(f"Sprite_To_CellType() not implemented for {sprite}")




class GameboardSpriteManager:

    def __init__(self, gameboard: GameBoard):
        self.gameboard = gameboard
        self.gameboard_sprites = np.empty(self.gameboard.gameboard.shape, dtype=sprite_dtype)


    def GetSprite(self, cell: Cell) -> Sprite:
        """
        Get the gameboard sprite for the given cell position.
        """
        pass

    def SetSprite(self, cell: Cell, cell_type: CellType) -> Sprite:
        """
        Replaces the cell location with cell_type.
        """
        pass





