import pygame
from SQ_modules.configs import CELL_DIMENSIONS, WHITE, Border_Size_Lookup
from SQ_modules.GameEnums import CellType, GameDifficulty
from SQ_modules.Sprites import Block, Ice, Goal, Player, HollowSquareSprite, Cell, SelectorTool, Highlighter, FindSpritesByLocation
from SQ_modules.DataTypes import Point, Size
from SQ_modules.GameEnums import CellType, GameDifficulty
from SQ_modules.GameBoard import GameBoard
from SQ_modules.LevelIO import LevelIO
from SQ_modules.configs import LEFT_CLICK, RIGHT_CLICK
from SQ_modules.my_logging import set_logger, log
from SQ_modules.Converters import PointToCell, CellToPoint
from SQ_modules.configs import WINDOW_DIMENSIONS, Border_Size_Lookup
import logging
set_logger()

@log
class ClickedCell:
    @log
    def __init__(self, cell: Cell, event: pygame.event.Event):
        """
        Initialize a ClickedCell object.

        Args:
            cell (pygame.Sprite): The cell object containing the sprite information.
        """
        self.cell = cell
        self.cell_type = self.cell.cellType
        self.cell_starting_position = self.cell.rect.center

        self.cell.offset_x = self.cell.rect.x - event.pos[0] if self.is_draggable() == True else None
        self.cell.offset_y = self.cell.rect.y - event.pos[1] if self.is_draggable() == True else None
    @log
    def is_draggable(self) -> bool:
        """
        Check if the cell is PLAYER or GOAL.

        Returns:
            bool: True if the cell is draggable; otherwise, False.
        """
        return self.cell_type in {CellType.PLAYER, CellType.GOAL}
    @log
    def is_cell(self) -> bool: #is this redundant with is_draggable()? Can this just be built into is_draggable()?
        """
        Check if the object represents a valid cell (not None or missing position).

        Returns:
            bool: True if the object represents a valid cell; otherwise, False.
        """
        return self.cell_type is not None and self.cell_starting_position is not None
    @log
    def handle_dragging(self, event: pygame.event.Event) -> bool: 
        """
        Handle dragging the cell when it is draggable.

        Args:
            event (pygame.Event): The mouse event containing the dragging information.

        This method handles the dragging behavior of the cell when it's draggable. It checks
        if the cell is draggable (PLAYER or GOAL) and updates its position according to the
        mouse event.

        Parameters:
            event (pygame.Event): The mouse event containing information about the dragging.
            
        Returns:
            bool: True if the cell is draggable and was updated; otherwise, False.
        """ 
        if self.is_draggable():
            self.cell.rect.x = event.pos[0] + self.cell.offset_x
            self.cell.rect.y = event.pos[1] + self.cell.offset_y



class LevelEditor:
    """
    Level editor class.


    Global state variables:
    self.drag_type
    self.offset
    self.initial_mouse_location
    """
    @log
    def __init__(self, gameboard: GameBoard, gameboard_sprite_group: pygame.sprite.LayeredUpdates, difficulty: GameDifficulty, player: Player, level_manager: LevelIO, screen: pygame.surface.Surface): #need from game, player, border_size, gameboard_sprite_group, gameboard, 
        self.screen = screen
        self.gameboard = gameboard
        self.player = player
        self.level_manager = level_manager
        self.gameboard_sprite_group = gameboard_sprite_group
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[self.difficulty]

        self.reset_click()
        self.create_pallet_sprites()
        self.selected_sprite_group = pygame.sprite.Group()

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



        self.selected_pallet_sprite = HollowSquareSprite(Point(CELL_DIMENSIONS.width, 150), 4)

        self.pallete_sprite_group = pygame.sprite.Group()
        self.pallete_sprite_group.add(self.select_tool_sprite)
        self.pallete_sprite_group.add(self.block_pallet_sprite)
        self.pallete_sprite_group.add(self.ice_pallet_sprite)
        self.pallete_sprite_group.add(self.selected_pallet_sprite)
        
        #self.highlighter_sprite_group.empty()
        #TEST
        # highlighter = Highlighter(Point(0, 0), Border_Size_Lookup[GameDifficulty.BEGINNER])
        # highlighter1 = Highlighter(Point(1, 1), Border_Size_Lookup[GameDifficulty.BEGINNER])
        # self.pallete_sprite_group.add(highlighter)
        # self.pallete_sprite_group.add(highlighter1)

    def reset_click(self):
        """
        Reset the global state of level editor. This mostly involves click variables to keep drag of dragging movements.
        """
        self.drag_type = None
        self.offset = None
        self.initial_mouse_location = None

        for sprite in self.gameboard_sprite_group:
            if isinstance(sprite, Goal):
                self.goal: Goal = sprite
                break

    def replace_gameboard_sprite(self, location: Cell, cell_type: CellType):
        """
        Replaces a sprite in the gameboard at `location` with a cell of type `cell_type`.

        Removes the old sprite and creates a new sprite.

        This method does no checking to make sure the user is not overwriting a cell they should not be.
        """
        #get all sprites at given location
        sprites = FindSpritesByLocation(self.gameboard_sprite_group, location)
        #shouldn't be possible to have more than 2 sprites at a location
        if len(sprites) > 2:
            raise RuntimeError(f"Found more than two sprites in gameboard with location {self.current_mouse_location}")
        #Shouldn't be possible to have 0 sprites at a location
        if len(sprites) == 0:
            raise RuntimeError(f"Found zero sprites in gameboard with location {self.current_mouse_location}")
        
        #this is a special case where you are replacing the cell type under the player
        if len(sprites) == 2:
            #check to make sure one of them is actually the player
            if sprites[0].cellType != CellType.PLAYER and sprites[1].cellType != CellType.PLAYER:
                raise RuntimeError(f"Neither of the sprites in gameboard at location {self.current_mouse_location} have type {CellType.PLAYER}.")
            else:
                #get the old sprite depending which is the player
                if sprites[0].cellType == CellType.PLAYER:
                    old_sprite = sprites[1]
                else:
                    old_sprite = sprites[0]
        #standard case - lenth is 1
        else: 
            old_sprite = sprites[0]

        #remove the old sprite
        self.gameboard_sprite_group.remove(old_sprite)

        #create new sprite based on the type, only BLOCK, ICE, and GOAL are implemented for now.
        if cell_type == CellType.BLOCK:
            new_sprite = Block(location, self.difficulty)
        elif cell_type == CellType.ICE:
            new_sprite = Ice(location, self.difficulty)
        elif cell_type == CellType.GOAL:
            new_sprite = Goal(location, self.difficulty)
            self.goal = new_sprite
        else:
            raise RuntimeError(f"Level Editor replace_gameboard_sprite not implemented for {self.drag_type}")
        #add new sprite to group.
        self.gameboard_sprite_group.add(new_sprite)
                    
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
        
    def handle_select(self):
        """
        Handles the creation of "highlight" sprites for the select tool.
        """
        #empty sprite group since all sprite will be added to the group again
        self.selected_sprite_group.empty()
        #iterate forwards if end location is higher, otherwise iterate backwards
        row_step = 1 if self.current_mouse_location.row >= self.initial_mouse_location.row else -1 
        col_step = 1 if self.current_mouse_location.col >= self.initial_mouse_location.col else -1
        #iterate from start to end for both rows and cols. Need to add the step size since the last index of range is ommitted.
        for row in range(self.initial_mouse_location.row, self.current_mouse_location.row + row_step, row_step):
            for col in range(self.initial_mouse_location.col, self.current_mouse_location.col + col_step, col_step):
                self.selected_sprite_group.add(Highlighter(Cell(row, col), self.difficulty))

    def handle_left_click(self, event: pygame.event.Event):
        """
        Handles the left click event for the level editor.
        """
        #handles if the block pallet was clicked
        self.check_for_pallet_click(event)
        #every left click will clear and selected cells
        self.selected_sprite_group.empty() 
        #save the current location of the mouse as the "initial location" for any dragging movements
        self.initial_mouse_location: Cell = PointToCell(Point(event.pos[0], event.pos[1]), self.difficulty)
        #also update the current mouse position, some methods rely on the current mouse position always being accurate
        self.current_mouse_location: Cell = PointToCell(Point(event.pos[0], event.pos[1]), self.difficulty)

        #if none, the click was outside the bounds of the gameboard.
        if self.initial_mouse_location is None:
            return

        #check if you clicked on the goal
        if self.gameboard.goal_pos == self.initial_mouse_location:
            self.offset: Point = Point(self.goal.rect.center[0] - event.pos[0], self.goal.rect.center[1] - event.pos[1]) # the offset is so your mouse and the goal maintain relative positioning while dragging
            self.drag_type = CellType.GOAL
        
        #check if you clicked on the player
        elif self.gameboard.player_pos == self.initial_mouse_location:
            self.offset: Point = Point(self.player.rect.center[0] - event.pos[0], self.player.rect.center[1] - event.pos[1]) # the offset is so your mouse and the player maintain relative positioning while dragging
            self.drag_type = CellType.PLAYER
        
        
        # check if the pallet is currently set to the "select" tool
        elif self.current_pallet_block == "SELECT":
            self.drag_type = "SELECT"
            self.selected_sprite_group.add(Highlighter(self.initial_mouse_location, self.difficulty)) #added initial clicked to highlighted cells sprite group
        
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
                self.replace_gameboard_sprite(self.current_mouse_location, self.drag_type)

    def handle_mouse_motion(self, event: pygame.event.Event):
        """
        Handles mouse motion event for level editor. This mostly consistly of any "dragging" operations.
        """
        #always update the current mouse location
        self.current_mouse_location: Cell = PointToCell(Point(event.pos[0], event.pos[1]), self.difficulty)
        #if drag type is none, then there is nothing that needs to be handled.
        if self.drag_type is None:
            return
        #this means that the mouse is off of the gameboard.
        if self.current_mouse_location is None:
            return
        #if you're dragging the player
        if self.drag_type==CellType.PLAYER:
            self.player.rect.center = Point(event.pos[0] + self.offset[0], event.pos[1] + self.offset[1])
        #if you're dragging the goal
        elif self.drag_type==CellType.GOAL:
            self.goal.rect.center = Point(event.pos[0] + self.offset[0], event.pos[1] + self.offset[1])
        #if the select tool is being used
        elif self.drag_type=="SELECT":
            self.handle_select()
        # handles any of the painting operations with the current pallet selection.
        else:
            if self.current_mouse_location is None:
                print()
            
            #if you are on top of the player or the goal, return and do not replace cell
            if self.current_mouse_location in [self.gameboard.player_pos, self.gameboard.Find_Goal_Pos()]:
                return
            if self.gameboard.Get_CellType(self.current_mouse_location) != self.drag_type:
                #update gameboard
                self.gameboard.UpdateCell(self.current_mouse_location, self.drag_type)
                #update sprite group
                self.replace_gameboard_sprite(self.current_mouse_location, self.drag_type)
    
    def handle_mouse_up(self, event: pygame.event.Event):
        """
        Handles the mouse up event for level editor. 

        This mostly involves verifying that player or goal has been dragged to an appropriate location.

        This also will reset all of the global states for level editor that are kept track of during dragging movements.
        """        
        #always update the current mouse location
        self.current_mouse_location: Cell = PointToCell(Point(event.pos[0], event.pos[1]), self.difficulty)


        if self.drag_type == CellType.PLAYER:
            #if mouse if off of gameboard - put back to original position
            if self.current_mouse_location is None:
                self.player.rect.center = CellToPoint(self.initial_mouse_location, self.difficulty)
            #player can only be "set down" on ice and ground.
            elif self.gameboard.Get_CellType(self.current_mouse_location) in [CellType.ICE, CellType.GROUND]: 
                #set new player position for gameboard
                self.gameboard.SetPlayerPos(self.current_mouse_location)
                #set new player position for sprite
                self.player.rect.center = CellToPoint(self.current_mouse_location, self.difficulty)
            #if operator tries to drop player on an "illegal" location, return the sprite to initial location.
            else:
                self.player.rect.center = CellToPoint(self.initial_mouse_location, self.difficulty)

        elif self.drag_type == CellType.GOAL:
            #if mouse if off of gameboard - put back to original position
            if self.current_mouse_location is None:
                self.goal.rect.center = CellToPoint(self.initial_mouse_location, self.difficulty)
            #we could allow putting of the goal anywhere, it's limited to ICE and GROUND right now.
            elif self.gameboard.Get_CellType(self.current_mouse_location) in [CellType.ICE, CellType.GROUND]: 
                #set old goal location to ICE, set new goal location to GOAL
                self.gameboard.UpdateCell(self.initial_mouse_location, CellType.ICE)
                self.gameboard.UpdateCell(self.current_mouse_location, CellType.GOAL)
                
                #fill ice in initial location
                self.replace_gameboard_sprite(self.initial_mouse_location, CellType.ICE)
                #put goal at new drop location
                self.replace_gameboard_sprite(self.current_mouse_location, CellType.GOAL)

            #if operator tries to drop player on an "illegal" location, return the sprite to initial location.
            else:
                self.goal.rect.center = CellToPoint(self.initial_mouse_location, self.difficulty)
        
        
        self.reset_click()

    def handle_button_down(self, event: pygame.event.Event):
        """
        Handles any button down events for level editor.
        """
        if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.level_manager.SaveInPlace(self.gameboard)
            logging.info("Map saved. (over-wrote level)")
        elif event.key == pygame.K_s:
            self.level_manager.SaveNew(self.gameboard)
            logging.info("Saved new map.")

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
        border_size = Border_Size_Lookup[self.level_manager.current_difficulty]
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
        self.gameboard_sprite_group.draw(self.screen)
        self.player.draw_player(self.screen)
        self.draw_grid()

            