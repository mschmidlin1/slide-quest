import pygame
from SQ_modules.configs import CELL_DIMENSIONS, WHITE, Border_Size_Lookup, LEFT_CLICK, RIGHT_CLICK, WINDOW_DIMENSIONS
from SQ_modules.game_enums import CellType, GameDifficulty
from SQ_modules.sprites import Block, Ice, Goal, Player, HollowSquareSprite, Cell, SelectorTool, Highlighter, FindSpritesByLocation, Ground
from SQ_modules.data_types import Point, Size
from SQ_modules.game_board import GameBoard
from SQ_modules.level_io import LevelIO, MapgenIO
from SQ_modules.my_logging import set_logger, log
from SQ_modules.converters import PointToCell, CellToPoint
from SQ_modules.gameboard_sprite_manager import GameboardSpriteManager
import logging
set_logger()

class LevelEditor:
    """
    Level editor class.


    Global state variables:
    self.drag_type
    self.offset
    self.initial_mouse_location
    """
    
    def __init__(self, gameboard: GameBoard, gameboard_sprite_manager: GameboardSpriteManager, screen: pygame.surface.Surface): #need from game, player, border_size, gameboard_sprite_group, gameboard, 
        self.screen = screen
        self.gameboard = gameboard
        self.gameboard_sprite_manager = gameboard_sprite_manager
        self.border_size = Border_Size_Lookup[self.gameboard.difficulty]

        self.reset_click()
        self.create_pallet_sprites()
        self.selected_sprite_group = pygame.sprite.Group()
        self.selected_cell_list = []

    def create_pallet_sprites(self):
        """
        Create the pallet and set current pallet block to CellType.BLOCK.
        """
        self.current_pallet_block: CellType = CellType.BLOCK

        self.select_tool_sprite = SelectorTool()
        self.select_tool_sprite.rect.center = Point(CELL_DIMENSIONS.width, 100)

        self.block_pallet_sprite = Block(Cell(0, 0),GameDifficulty.BEGINNER) #the constructor arguments don't matter because we're gonna set the location manually
        self.block_pallet_sprite.rect.center = Point(CELL_DIMENSIONS.width, 150)

        self.ice_pallet_sprite = Ice(Cell(0, 0), GameDifficulty.BEGINNER) #the constructor arguments don't matter because we're gonna set the location manually
        self.ice_pallet_sprite.rect.center = Point(CELL_DIMENSIONS.width, 200)

        self.ground_pallet_sprite = Ground(Cell(0, 0), GameDifficulty.BEGINNER) #the constructor arguments don't matter because we're gonna set the location manually
        self.ground_pallet_sprite.rect.center = Point(CELL_DIMENSIONS.width, 250)

        self.selected_pallet_sprite = HollowSquareSprite(Point(CELL_DIMENSIONS.width, 150), 4)

        self.pallete_sprite_group = pygame.sprite.Group()
        self.pallete_sprite_group.add(self.select_tool_sprite)
        self.pallete_sprite_group.add(self.block_pallet_sprite)
        self.pallete_sprite_group.add(self.ice_pallet_sprite)
        self.pallete_sprite_group.add(self.selected_pallet_sprite)
        self.pallete_sprite_group.add(self.ground_pallet_sprite)

    def reset_click(self):
        """
        Reset the global state of level editor. This mostly involves click variables to keep drag of dragging movements.
        """
        self.drag_type = None
        self.offset = None
        self.initial_mouse_location = None
                    
    def check_for_pallet_click(self, event: pygame.event.Event):
        """
        Checks to see if any sprites in the block pallet have been clicked.

        If something in the pallet has been clicked, update the current_pallet_block property.

        """
        if self.select_tool_sprite.rect.collidepoint(event.pos):
            self.current_pallet_block = "SELECT"
            self.selected_pallet_sprite.rect.center = self.select_tool_sprite.rect.center
            logging.info("Pallet block changed to SELECT.")
        elif self.block_pallet_sprite.rect.collidepoint(event.pos):
            self.current_pallet_block = CellType.BLOCK
            self.selected_pallet_sprite.rect.center = self.block_pallet_sprite.rect.center
            logging.info("Pallet block changed to BLOCK.")
        elif self.ice_pallet_sprite.rect.collidepoint(event.pos):
            self.current_pallet_block = CellType.ICE
            self.selected_pallet_sprite.rect.center = self.ice_pallet_sprite.rect.center
            logging.info("Pallet block changed to ICE.")
        elif self.ground_pallet_sprite.rect.collidepoint(event.pos):
            self.current_pallet_block = CellType.GROUND
            self.selected_pallet_sprite.rect.center = self.ground_pallet_sprite.rect.center
        
    def handle_select(self):
        """
        Handles the creation of "highlight" sprites for the select tool.
        """
        #empty sprite group since all sprite will be added to the group again
        self.selected_sprite_group.empty()
        #empty cell list since all sprites will be added to the group again
        self.selected_cell_list = []
        #iterate forwards if end location is higher, otherwise iterate backwards
        row_step = 1 if self.current_mouse_location.row >= self.initial_mouse_location.row else -1 
        col_step = 1 if self.current_mouse_location.col >= self.initial_mouse_location.col else -1
        #iterate from start to end for both rows and cols. Need to add the step size since the last index of range is ommitted.
        for row in range(self.initial_mouse_location.row, self.current_mouse_location.row + row_step, row_step):
            for col in range(self.initial_mouse_location.col, self.current_mouse_location.col + col_step, col_step):
                new_loc = Cell(row, col)
                self.selected_cell_list.append(new_loc)
                self.selected_sprite_group.add(Highlighter(new_loc, self.gameboard.difficulty))

    def handle_left_click(self, event: pygame.event.Event):
        """
        Handles the left click event for the level editor.
        """
        #handles if the block pallet was clicked
        self.check_for_pallet_click(event)
        #every left click will clear and selected cells
        self.selected_sprite_group.empty() 
        #save the current location of the mouse as the "initial location" for any dragging movements
        self.initial_mouse_location: Cell = PointToCell(Point(event.pos[0], event.pos[1]), self.gameboard.difficulty)
        #also update the current mouse position, some methods rely on the current mouse position always being accurate
        self.current_mouse_location: Cell = PointToCell(Point(event.pos[0], event.pos[1]), self.gameboard.difficulty)

        #if none, the click was outside the bounds of the gameboard.
        if self.initial_mouse_location is None:
            return

        #check if you clicked on the goal
        if self.gameboard.goal_pos == self.initial_mouse_location:
            self.offset: Point = Point(self.gameboard_sprite_manager.goal_sprite.rect.center[0] - event.pos[0], self.gameboard_sprite_manager.goal_sprite.rect.center[1] - event.pos[1]) # the offset is so your mouse and the goal maintain relative positioning while dragging
            self.drag_type = CellType.GOAL
        
        #check if you clicked on the player
        elif self.gameboard.player_pos == self.initial_mouse_location:
            self.offset: Point = Point(self.gameboard_sprite_manager.player_sprite.rect.center[0] - event.pos[0], self.gameboard_sprite_manager.player_sprite.rect.center[1] - event.pos[1]) # the offset is so your mouse and the player maintain relative positioning while dragging
            self.drag_type = CellType.PLAYER
        
        
        # check if the pallet is currently set to the "select" tool
        elif self.current_pallet_block == "SELECT":
            self.drag_type = "SELECT"
            self.handle_select()
        
        # this else contains the logic for "painting" depending on which pallet block is currently chosen
        else:
            self.drag_type = self.current_pallet_block
            #if you are on top of the player or the goal, return and do not replace cell
            if self.current_mouse_location in [self.gameboard.player_pos, self.gameboard.Find_Goal_Pos()]:
                return
            if self.gameboard.Get_CellType(self.initial_mouse_location) != self.current_pallet_block:
                #update gameboard
                self.gameboard.UpdateCell(self.current_mouse_location, self.drag_type)
                #update sprite group
                self.gameboard_sprite_manager.SetSprite(self.current_mouse_location, self.drag_type)

    def handle_mouse_motion(self, event: pygame.event.Event):
        """
        Handles mouse motion event for level editor. This mostly consistly of any "dragging" operations.
        """
        #always update the current mouse location
        self.current_mouse_location: Cell = PointToCell(Point(event.pos[0], event.pos[1]), self.gameboard.difficulty)
        #if drag type is none, then there is nothing that needs to be handled.
        if self.drag_type is None:
            return
        #this means that the mouse is off of the gameboard.
        if self.current_mouse_location is None:
            return
        #if you're dragging the player
        if self.drag_type==CellType.PLAYER:
            self.gameboard_sprite_manager.player_sprite.rect.center = Point(event.pos[0] + self.offset[0], event.pos[1] + self.offset[1])
        #if you're dragging the goal
        elif self.drag_type==CellType.GOAL:
            self.gameboard_sprite_manager.goal_sprite.rect.center = Point(event.pos[0] + self.offset[0], event.pos[1] + self.offset[1])
        #if the select tool is being used
        elif self.drag_type=="SELECT":
            self.handle_select()
        # handles any of the painting operations with the current pallet selection.
        else:
            #if you are on top of the player or the goal, return and do not replace cell
            if self.current_mouse_location in [self.gameboard.player_pos, self.gameboard.Find_Goal_Pos()]:
                return
            if self.gameboard.Get_CellType(self.current_mouse_location) != self.drag_type:
                #update gameboard
                self.gameboard.UpdateCell(self.current_mouse_location, self.drag_type)
                #update sprite group
                self.gameboard_sprite_manager.SetSprite(self.current_mouse_location, self.drag_type)
    
    def handle_mouse_up(self, event: pygame.event.Event):
        """
        Handles the mouse up event for level editor. 

        This mostly involves verifying that player or goal has been dragged to an appropriate location.

        This also will reset all of the global states for level editor that are kept track of during dragging movements.
        """        
        #always update the current mouse location
        self.current_mouse_location: Cell = PointToCell(Point(event.pos[0], event.pos[1]), self.gameboard.difficulty)


        if self.drag_type == CellType.PLAYER:
            #if mouse if off of gameboard - put back to original position
            if self.current_mouse_location is None:
                self.gameboard_sprite_manager.player_sprite.rect.center = CellToPoint(self.initial_mouse_location, self.gameboard.difficulty)
            #player can only be "set down" on ice and ground.
            elif self.gameboard.Get_CellType(self.current_mouse_location) in [CellType.ICE, CellType.GROUND]: 
                #set new player position for gameboard
                self.gameboard.SetPlayerPos(self.current_mouse_location)
                #set new player position for sprite
                self.gameboard_sprite_manager.player_sprite.rect.center = CellToPoint(self.current_mouse_location, self.gameboard.difficulty)
            #if operator tries to drop player on an "illegal" location, return the sprite to initial location.
            else:
                self.gameboard_sprite_manager.player_sprite.rect.center = CellToPoint(self.initial_mouse_location, self.gameboard.difficulty)

        elif self.drag_type == CellType.GOAL:
            #if mouse if off of gameboard - put back to original position
            if self.current_mouse_location is None:
                self.gameboard_sprite_manager.goal_sprite.rect.center = CellToPoint(self.initial_mouse_location, self.gameboard.difficulty)
            #we could allow putting of the goal anywhere, it's limited to ICE and GROUND right now.
            elif self.gameboard.Get_CellType(self.current_mouse_location) in [CellType.ICE, CellType.GROUND]: 
                #set old goal location to ICE, set new goal location to GOAL
                self.gameboard.UpdateCell(self.initial_mouse_location, CellType.ICE)
                self.gameboard.UpdateCell(self.current_mouse_location, CellType.GOAL)
                
                #fill ice in initial location
                self.gameboard_sprite_manager.SetSprite(self.initial_mouse_location, CellType.ICE)
                #put goal at new drop location
                self.gameboard_sprite_manager.SetSprite(self.current_mouse_location, CellType.GOAL)

            #if operator tries to drop player on an "illegal" location, return the sprite to initial location.
            else:
                self.gameboard_sprite_manager.goal_sprite.rect.center = CellToPoint(self.initial_mouse_location, self.gameboard.difficulty)
        
        
        self.reset_click()

    def handle_button_down(self, event: pygame.event.Event):
        """
        Handles any button down events for level editor.
        """

        #pressing just the "s" key
        if event.key == pygame.K_s:
            #if the level editor has a selected region, save that
            if len(self.selected_cell_list)!=0:
                min_row = min(self.selected_cell_list, key=lambda cell: cell.row).row
                max_row = max(self.selected_cell_list, key=lambda cell: cell.row).row

                min_col = min(self.selected_cell_list, key=lambda cell: cell.col).col
                max_col = max(self.selected_cell_list, key=lambda cell: cell.col).col

                upper_left = Cell(min_row, min_col)
                lower_right = Cell(max_row, max_col)

                sub_array = self.gameboard.Crop(upper_left, lower_right)
                MapgenIO.SaveMapgen(sub_array)

    def update(self, events: list[pygame.event.Event]):
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    self.handle_left_click(event)
                
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
                                
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
                
            elif event.type == pygame.KEYDOWN:
                self.handle_button_down(event)

        self.pallete_sprite_group.update()
        self.selected_sprite_group.update()
    
    def draw_grid(self):
        """
        This is just temporary for showing the dimensions of the grid until we can start implementing sprites more regularly
        """
        border_size = Border_Size_Lookup[self.gameboard.difficulty]
        for x in range(border_size.width, WINDOW_DIMENSIONS.width-border_size.width + 1, CELL_DIMENSIONS.width):
            pygame.draw.line(self.screen, WHITE, (x, border_size.height), (x, WINDOW_DIMENSIONS.height-border_size.height))
        for y in range(border_size.height, WINDOW_DIMENSIONS.height-border_size.height + 1, CELL_DIMENSIONS.height):
            pygame.draw.line(self.screen, WHITE, (border_size.width, y), (WINDOW_DIMENSIONS.width-border_size.width, y))

    def draw(self):
        """
        Handles draing of all level editor sprites.
        """
        self.pallete_sprite_group.draw(self.screen)
        self.selected_sprite_group.draw(self.screen)
        #self.gameboard_sprite_manager.draw()
        self.draw_grid()

            