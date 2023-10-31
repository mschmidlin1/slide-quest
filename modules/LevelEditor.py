import pygame
from modules.GameEnums import CellType
from modules.Sprites import Block, Ice, Player, Goal
from modules.Point import Point
from modules.GameEnums import CellType
from modules.MapConverter import update_map
from modules.configs import CURRENT_DIFFICULTY

class LevelEditor():
    def __init__(self, window):
        self.dragging_left = False
        self.dragging_right = False  
        self.draggingPlayer = False
        self.draggingGoal = False
        self.top_cell = None
        self.clicked_cells = None
        self.dragged_cell = None
        self.curr_pos = None
        self.window  = window
        self.current_game = window.current_game
        self.player = self.current_game.player

    def update_gameboard(self):
        self.current_game.update_map_text()
        update_map(CURRENT_DIFFICULTY)
        self.current_game.gameboard.ReadBoard('levels\\advanced\\map.csv')

    def debugging(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:

                self.clicked_cells = [clicked_cell for clicked_cell in self.current_game.gameboard_sprite_group if clicked_cell.rect.collidepoint(event.pos)]
                
                if self.clicked_cells:
                    self.top_cell = self.clicked_cells[-1]
                    self.curr_pos = self.top_cell.Get_Cell_Current_Position(self.top_cell.rect.center)

                    if event.button == 1:  # LEFT CLICK

                        self.dragging_left = True

                        if self.top_cell.cellType == CellType.ICE:
                            # print(f"Cell {top_cell.cellType} clicked at: {curr_pos} ... converting to {CellType.BLOCK}")
                            self.current_game.gameboard_sprite_group.remove(self.top_cell)
                            self.current_game.gameboard_sprite_group.add(Block(self.curr_pos, self.current_game.border_width, self.current_game.border_height))

                        elif self.top_cell.cellType == CellType.PLAYER:
                            self.draggingPlayer = True
                            self.top_cell.offset_x, self.top_cell.offset_y = self.top_cell.rect.x - event.pos[0], self.top_cell.rect.y - event.pos[1]

                        elif self.top_cell.cellType == CellType.GOAL:
                            self.draggingGoal = True
                            self.top_cell.offset_x, self.top_cell.offset_y = self.top_cell.rect.x - event.pos[0], self.top_cell.rect.y - event.pos[1]

                    if event.button == 3:  # RIGHT CLICK
                        self.dragging_right = True
                        if self.top_cell.cellType == CellType.BLOCK:
                            # print(f"Cell {top_cell.cellType} clicked at: {curr_pos} ... converting to {CellType.ICE}")
                            self.current_game.gameboard_sprite_group.remove(self.top_cell)
                            self.current_game.gameboard_sprite_group.add(Ice(self.curr_pos, self.current_game.border_width, self.current_game.border_height))

            elif event.type == pygame.MOUSEMOTION:
                if self.draggingPlayer:
                    self.top_cell.rect.x = event.pos[0] + self.top_cell.offset_x
                    self.top_cell.rect.y = event.pos[1] + self.top_cell.offset_y

                if self.draggingGoal:
                    
                    self.top_cell.rect.x = event.pos[0] + self.top_cell.offset_x
                    self.top_cell.rect.y = event.pos[1] + self.top_cell.offset_y

                elif self.dragging_left:
                    self.clicked_cells = [clicked_cell for clicked_cell in self.current_game.gameboard_sprite_group if clicked_cell.rect.collidepoint(event.pos)]

                    for cell in self.current_game.gameboard_sprite_group:
                        if cell.rect.collidepoint(event.pos):
                            self.dragged_cell = self.clicked_cells[-1]
                            if cell.cellType == CellType.ICE and len(self.clicked_cells) == 1:
                                self.current_game.gameboard_sprite_group.remove(self.dragged_cell)
                                self.current_game.gameboard_sprite_group.add(Block(self.dragged_cell.Get_Cell_Current_Position(self.dragged_cell.rect.center), self.current_game.border_width, self.current_game.border_height))

                elif self.dragging_right:
                    self.clicked_cells = [clicked_cell for clicked_cell in self.current_game.gameboard_sprite_group if clicked_cell.rect.collidepoint(event.pos)]
                    
                    for cell in self.current_game.gameboard_sprite_group:
                        if cell.rect.collidepoint(event.pos):
                            self.dragged_cell = self.clicked_cells[-1]
                            if cell.cellType == CellType.BLOCK:
                                self.current_game.gameboard_sprite_group.remove(self.dragged_cell)
                                self.current_game.gameboard_sprite_group.add(Ice(self.dragged_cell.Get_Cell_Current_Position(self.dragged_cell.rect.center), self.current_game.border_width, self.current_game.border_height))
                                
            elif event.type == pygame.MOUSEBUTTONUP:
                #might be able to make this one dragging and handle goal / player within
                if self.draggingPlayer:
                    self.draggingPlayer = False
                    self.dragged_cells = [clicked_cell for clicked_cell in self.current_game.gameboard_sprite_group if clicked_cell.rect.collidepoint(event.pos)]
                    cell_beneath_player = self.dragged_cells[0]
                    if cell_beneath_player.cellType == CellType.BLOCK or cell_beneath_player.cellType == CellType.GOAL:
                        self.top_cell.rect.center = self.top_cell.GameboardCell_To_CenterPixelCoords(self.curr_pos)
                    elif cell_beneath_player.cellType == CellType.ICE: # or ground
                        self.current_game.gameboard_sprite_group.remove(self.top_cell)
                        self.current_game.gameboard.player_pos = Point(cell_beneath_player.Get_Cell_Current_Position(cell_beneath_player.rect.center)[0], cell_beneath_player.Get_Cell_Current_Position(cell_beneath_player.rect.center)[1])
                        self.current_game.player.rect.center = cell_beneath_player.rect.center
                        self.current_game.gameboard_sprite_group.add(self.player)
                    else:
                        self.top_cell.rect.center = self.top_cell.GameboardCell_To_CenterPixelCoords(self.curr_pos)
                        
                if self.draggingGoal:
                    self.draggingGoal = False
                    self.dragged_cells = [clicked_cell for clicked_cell in self.current_game.gameboard_sprite_group if clicked_cell.rect.collidepoint(event.pos)]
                    cell_beneath_goal = self.dragged_cells[0]
                    if cell_beneath_goal.cellType == CellType.BLOCK or cell_beneath_goal.cellType == CellType.PLAYER:
                        self.top_cell.rect.center = self.top_cell.GameboardCell_To_CenterPixelCoords(self.curr_pos)
                    elif cell_beneath_goal.cellType == CellType.ICE and not len(self.dragged_cells) == 3: # or ground
                        self.current_game.gameboard_sprite_group.remove(self.clicked_cells[-1])
                        self.current_game.gameboard_sprite_group.add(Goal(self.top_cell.Get_Cell_Current_Position(event.pos), self.current_game.border_width, self.current_game.border_height))
                        self.current_game.gameboard_sprite_group.remove(self.dragged_cells[0])
                        self.current_game.gameboard_sprite_group.add(Ice(self.curr_pos, self.current_game.border_width, self.top_cell.border_height))
                    else:
                        self.top_cell.rect.center = self.top_cell.GameboardCell_To_CenterPixelCoords(self.curr_pos)
                            
                self.__init__(self.window)

                self.update_gameboard()
