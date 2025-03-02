import pygame
from pygame.sprite import Sprite
from sq_src.configs import CELL_DIMENSIONS, WINDOW_DIMENSIONS
from sq_src.data_structures.converters import CellToPoint, IsPointInGameboard, PointToCell
from sq_src.data_structures.data_types import Cell, Point
from sq_src.data_structures.game_enums import CellType, Direction, GameDifficulty
from sq_src.core.game_board import GameBoard
import numpy as np

from sq_src.sprites.background_spites import Block, Goal, Ice
from sq_src.sprites.player import Player
from sq_src.sprites.snow import GroundSnow
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
        return GroundSnow
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
    elif sprite == GroundSnow:
        return CellType.GROUND
    else:
        raise NotImplementedError(f"Sprite_To_CellType() not implemented for {sprite}")

class GameboardSpriteManager:

    def __init__(self, gameboard: GameBoard, screen: pygame.surface.Surface):
        self.gameboard = gameboard
        self.screen = screen
        self.gameboard_sprites = np.empty(self.gameboard.gameboard.shape, dtype=sprite_dtype)
        self.gameboard_sprite_group = pygame.sprite.LayeredUpdates()
        self.background_ice_sprites = pygame.sprite.LayeredUpdates()
        self.player_sprite: Player = None

        self.PopulateSprites()
        self.CreatePlayerSprite()
        self.fill_background()

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
                layer = 1
                if cell == CellType.ICE:
                    layer = 1
                elif cell == CellType.GROUND:
                    layer = 2
                elif cell == CellType.BLOCK:
                    layer = 3
                else:
                    layer=4
                self.gameboard_sprite_group.add(new_sprite, layer=layer)
    
    def fill_background(self):
        for y in range(0, WINDOW_DIMENSIONS.height, CELL_DIMENSIONS.height):
            for x in range(0, WINDOW_DIMENSIONS.width, CELL_DIMENSIONS.width):
                if IsPointInGameboard(Point(x, y), self.gameboard.difficulty):
                    self.background_ice_sprites.add(Ice(PointToCell(Point(x,y), self.gameboard.difficulty), self.gameboard.difficulty))
                 
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

    def Move(self, cell: Cell, direction):
        """
        Moves the player in a given direction.
        """
        self.player_sprite.move(cell, direction)

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
        self.background_ice_sprites.draw(self.screen)
        self.gameboard_sprite_group.draw(self.screen)
        self.player_sprite.draw_player(self.screen)






