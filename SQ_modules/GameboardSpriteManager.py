import pygame
from pygame.sprite import Sprite
from SQ_modules.Converters import CellToPoint
from SQ_modules.DataTypes import Cell
from SQ_modules.GameEnums import CellType, Direction, GameDifficulty
from SQ_modules.GameBoard import GameBoard
import numpy as np
from SQ_modules.Sprites import Player, Goal, Block, Ice, Ground
sprite_dtype = np.dtype(Sprite)


def CellType_To_SpriteType(cell_type: CellType) -> Sprite:
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
    elif cell_type == CellType.GROUND:
        return Ground
    else:
        raise NotImplementedError(f"CellType_To_Sprite() not implemented for {cell_type}")
    
def SpriteType_To_CellType(sprite: Sprite) -> CellType:
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
    elif sprite == Ground:
        return CellType.GROUND
    else:
        raise NotImplementedError(f"Sprite_To_CellType() not implemented for {sprite}")

class GameboardSpriteManager:

    def __init__(self, gameboard: GameBoard, screen: pygame.surface.Surface):
        self.gameboard = gameboard
        self.screen = screen
        self.gameboard_sprites = np.empty(self.gameboard.gameboard.shape, dtype=sprite_dtype)
        self.gameboard_sprite_group = pygame.sprite.LayeredUpdates()
        self.player_sprite: Player = None

        self.PopulateSprites()
        self.CreatePlayerSprite()

        self.goal_sprite: Goal = self.GetGoalSprite()

    def CreatePlayerSprite(self):
        """"
        Creates the player sprite.
        """
        self.player_sprite = Player(self.gameboard.player_pos, self.gameboard.difficulty)

    def PopulateSprites(self):
        """
        Populates the gameboard sprites using the self.gameboard property.
        self.gameboard_sprites will be filled in by the end of this method.
        """
        for row_num, cells in enumerate(self.gameboard.gameboard):
            for col_num, cell in enumerate(cells):
                sprite_type = CellType_To_SpriteType(cell)
                new_sprite = sprite_type(Cell(row_num, col_num), self.gameboard.difficulty)
                self.gameboard_sprites[row_num, col_num] = new_sprite
                self.gameboard_sprite_group.add(new_sprite)
                 
    def GetSprite(self, cell: Cell) -> Sprite:
        """
        Get the gameboard sprite for the given cell position.
        """
        return self.gameboard_sprites[cell.row, cell.col]

    def GetCellType(self, cell: Cell) -> CellType:
        """
        Gets the celltype of the given cell location.
        """

        return SpriteType_To_CellType(type(self.GetSprite(cell)))

    def Move(self, cell: Cell):
        """
        Moves the player in a given direction.
        """
        self.player_sprite.move(cell)

    def SetSprite(self, cell: Cell, cell_type: CellType) -> None:
        """
        Replaces the cell location with a sprite of cell_type.
        """
        #if cell type is player, just set the player sprite to the new location
        if cell_type == CellType.PLAYER:
            self.player_sprite.rect.center = CellToPoint(cell, self.gameboard.difficulty)
            return
        
        #get the old sprite object from the location and delete from gameboard group
        old_sprite = self.GetSprite(cell)
        self.gameboard_sprite_group.remove(old_sprite)

        #create new sprite, set in gameboard array, and add to gameboard sprite group
        new_cell_type = CellType_To_SpriteType(cell_type)
        new_sprite = new_cell_type(cell, self.gameboard.difficulty)
        self.gameboard_sprites[cell.row, cell.col] = new_sprite
        self.gameboard_sprite_group.add(new_sprite)

        if cell_type == CellType.GOAL:
            self.goal_sprite = new_sprite

    def GetGoalSprite(self) -> Sprite:
        """
        Get's the goal sprite object.
        """
        return self.GetSprite(self.gameboard.Find_Goal_Pos())

    def update(self, events: list[pygame.event.Event]):
        """
        Handles all updates for Gameboard sprites.
        """
        self.gameboard_sprite_group.update()
        self.player_sprite.update()

    def draw(self):
        """
        Handles drawing of all gameboard sprites.
        """
        self.gameboard_sprite_group.draw(self.screen)
        self.player_sprite.draw_player(self.screen)






