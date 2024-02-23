import pygame
from modules.configs import CELL_DIMENSIONS, WHITE
from modules.GameEnums import CellType
from modules.Sprites import Block, Ice, Goal, Player, HollowSquareSprite, Cell
from modules.DataTypes import Point, Size
from modules.GameEnums import CellType, GameDifficulty
from modules.GameBoard import GameBoard
from modules.LevelIO import LevelIO
from modules.configs import LEFT_CLICK, RIGHT_CLICK
from modules.my_logging import set_logger, log
from modules.configs import WINDOW_DIMENSIONS, Border_Size_Lookup
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
@log
class LevelEditor:
    @log
    def __init__(self, gameboard: GameBoard, gameboard_sprite_group: pygame.sprite.LayeredUpdates, border_size: Size, player: Player, level_manager: LevelIO, screen: pygame.surface.Surface): #need from game, player, border_size, gameboard_sprite_group, gameboard, 
        self.screen = screen
        self.gameboard = gameboard
        self.player = player
        self.level_manager = level_manager
        self.gameboard_sprite_group = gameboard_sprite_group
        self.border_size = border_size

        self.reset_click()

        self.current_pallet_block: CellType = CellType.BLOCK

        self.block_pallet_sprite = Block(Point(0, 0), Border_Size_Lookup[GameDifficulty.BEGINNER]) #the constructor arguments don't matter because we're gonna set the location manually
        self.block_pallet_sprite.rect.center = Point(60, WINDOW_DIMENSIONS.height-30)

        self.ice_pallet_sprite = Ice(Point(0, 0), Border_Size_Lookup[GameDifficulty.BEGINNER]) #the constructor arguments don't matter because we're gonna set the location manually
        self.ice_pallet_sprite.rect.center = Point(120, WINDOW_DIMENSIONS.height-30)

        self.selected_pallet_sprite = HollowSquareSprite(Point(60, WINDOW_DIMENSIONS.height-30), 4)

        self.pallete_sprite_group = pygame.sprite.Group()
        self.pallete_sprite_group.add(self.block_pallet_sprite)
        self.pallete_sprite_group.add(self.ice_pallet_sprite)
        self.pallete_sprite_group.add(self.selected_pallet_sprite)
    @log
    def reset_click(self):
        """
        Reset clickedcell, click_type, and new_cell to None.
        """
        self.clickedcell = None
        self.click_type = None
        self.new_cell = None

    @log
    def replace_cell(self, old_cell: pygame.sprite.Sprite, new_cell_type: CellType, event: pygame.event.Event):
        """
        Replace a cell with a new cell of the specified type.

        Args:
            old_cell (pygame.Sprite): The cell to be replaced.
            new_cell_type (CellType): The type of the new cell to replace the old one.
            event (pygame.Event): The mouse event containing information about the replacement.

        This method replaces a cell in the gameboard with a new cell of the specified type.
        The replacement depends on the `new_cell_type` provided. It also takes into account
        specific conditions for replacing cells, such as ensuring that player and goal cells
        are not replaced.

        Parameters:
            old_cell (pygame.Sprite): The cell to be replaced.
            new_cell_type (CellType): The type of the new cell to replace the old one.
            event (pygame.Event): The mouse event containing information about the replacement.
        """
        if old_cell.cellType == new_cell_type or old_cell.cellType in {CellType.PLAYER, CellType.GOAL} :
            return

        if self.current_pallet_block == CellType.BLOCK:
            self.new_cell = Block(old_cell.Get_Cell_Current_Position(event.pos), self.border_size)
        elif self.current_pallet_block == CellType.ICE:
            self.new_cell = Ice(old_cell.Get_Cell_Current_Position(event.pos), self.border_size)
        
        # grab the gameboard coords you're working with
        temp_pos = Point(*old_cell.Get_Cell_Current_Position(event.pos))
        # update gameboard object
        self.gameboard.UpdateCell(temp_pos, new_cell_type)
        # elif new_cell_type == CellType.GOAL:
        #     self.new_cell = Goal(old_cell.Get_Cell_Current_Position(event.pos), self.current_game.border_width, self.current_game.border_height)

        # if self.new_cell:
        self.gameboard_sprite_group.remove(old_cell)
        self.gameboard_sprite_group.add(self.new_cell)
        # self.replaced_cells.add(old_cell)
    @log
    def move_goal(self, old_cell, new_cell):
        """
        Move a goal cell from an old position to a new position on the gameboard.

        Args:
            old_cell (ClickedCell): The ClickedCell representing the old position of the goal cell.
            new_cell (ClickedCell): The ClickedCell representing the new position to move the goal cell to.

        This method is used to move a goal cell from its old position to a new position on the gameboard.
        It checks if the old_cell represents a goal cell and performs the following actions:
        1. Removes the new_cell from the gameboard if it exists.
        2. Adds a new Goal cell at the position of the old_cell.
        3. Removes the old_cell from the gameboard.
        4. Adds an Ice cell at the old position of the goal cell.

        Parameters:
            old_cell (ClickedCell): The ClickedCell representing the old goal cell position.
            new_cell (ClickedCell): The ClickedCell representing the new position to move the goal cell to.
        """
        if old_cell.cell_type != CellType.GOAL:
            return
        self.gameboard_sprite_group.remove(new_cell.cell)
        self.gameboard_sprite_group.add(Goal(old_cell.cell.Get_Cell_Current_Position(new_cell.cell.rect.center), self.border_size))
        self.gameboard_sprite_group.remove(old_cell.cell)
        self.gameboard_sprite_group.add(Ice(new_cell.cell.Get_Cell_Current_Position(old_cell.cell_starting_position), self.border_size))

        #update the gameboard with the new goal position
        #fill the cell under the old goal position with Ice
        current_goal_pos: Point = self.gameboard.Find_Goal_Pos()
        self.gameboard.UpdateCell(current_goal_pos, CellType.ICE)
        new_goal_pos = Point(*old_cell.cell.Get_Cell_Current_Position(new_cell.cell.rect.center))
        self.gameboard.UpdateCell(new_goal_pos, CellType.GOAL)
    @log
    def update_cell_after_dragging(self, dragging_cell, underneath_cell, underneath_goal):
        """
        Update cell positions and interactions after a cell is dragged and released.

        Args:
            dragging_cell (ClickedCell): The ClickedCell representing the cell being dragged.
            underneath_cell (ClickedCell): The ClickedCell representing the cell underneath the dragged cell.
            event (pygame.Event): The mouse event containing information about the drag release.

        This method handles the interactions that occur after a cell has been dragged and released.
        It takes two ClickedCell objects, dragging_cell (the cell being dragged) and underneath_cell (the cell
        under the dragged cell), and an event that describes the drag release.

        If the dragging_cell represents a PLAYER:
        - If the underneath_cell is ICE, the dragging_cell is placed at the center of the underneath_cell,
        and the player position in the gameboard is updated accordingly.
        - If the underneath_cell is not ICE, the dragging_cell is placed back at its starting position.

        If the dragging_cell represents a GOAL:
        - If the underneath_cell is ICE, the goal is moved to the underneath_cell's position, and an ICE cell
        is placed at the dragging_cell's old position.
        - If the underneath_cell is not ICE, the dragging_cell is placed back at its starting position.

        Parameters:
            dragging_cell (ClickedCell): The ClickedCell representing the cell being dragged.
            underneath_cell (ClickedCell): The ClickedCell representing the cell under the dragged cell.
            event (pygame.Event): The mouse event describing the drag release.
        """
        if dragging_cell.cell_type == CellType.PLAYER:
            if underneath_cell.cell_type == CellType.ICE:
                dragging_cell.cell.rect.center = underneath_cell.cell.rect.center
                self.gameboard.player_pos = Point(dragging_cell.cell.Get_Cell_Current_Position(underneath_cell.cell.rect.center)[0], dragging_cell.cell.Get_Cell_Current_Position(underneath_cell.cell.rect.center)[1])
            else:
                self.place_cell_at_starting_position(dragging_cell)
        elif dragging_cell.cell_type == CellType.GOAL:
            if underneath_cell.cell_type == CellType.ICE and underneath_goal.cell_type != CellType.PLAYER:
                self.move_goal(dragging_cell, underneath_cell)

            else:
                self.place_cell_at_starting_position(dragging_cell)
    @log
    def place_cell_at_starting_position(self, dragging_cell):
        """
        Place a cell back to its starting position.

        Args:
            dragging_cell (ClickedCell): The ClickedCell representing the cell being dragged.

        This method takes a ClickedCell object representing a cell and moves it back to its
        original starting position within the gameboard. It is used to reset the cell's position
        when the user cancels the cell's dragging operation or places it in an invalid location.

        Parameters:
            dragging_cell (ClickedCell): The ClickedCell representing the cell being dragged.
        """
        dragging_cell.cell.rect.center = dragging_cell.cell_starting_position
    @log
    def handle_mouse_click(self, clicked_cell: pygame.sprite.Sprite, click_type: int, event: pygame.event.Event):
        """
        Handle mouse clicks on cells in the gameboard.

        Args:
            clicked_cell (ClickedCell): The clicked cell object representing the selected cell.
            event (pygame.Event): The mouse event containing information about the click.
            click_type (int): The type of mouse click (LEFT_CLICK or RIGHT_CLICK).

        This method handles the different actions associated with left and right mouse clicks
        on cells within the gameboard. It checks the type of the clicked cell and the click type
        to perform the appropriate action.

        If the left mouse button is clicked:
        - If the clicked cell is ICE, it is converted to BLOCK.
        - For other cell types, it checks if they are draggable, and if so,
        initiates dragging of the cell.

        If the right mouse button is clicked:
        - If the clicked cell is BLOCK, it is converted to ICE.

        The method also contains a placeholder for a method to update cells, which can be added
        in the future to centralize the logic for cell updates.

        This method provides a central point for handling various cell interactions based on
        the mouse click type.
        """
        self.click_type = click_type
        
        if self.click_type == LEFT_CLICK:  # LEFT CLICK
            if clicked_cell.cell_type not in [self.current_pallet_block, CellType.GOAL, CellType.PLAYER]:#need to check if we're on player?
                self.replace_cell(clicked_cell.cell, self.current_pallet_block, event)

        # if self.click_type == RIGHT_CLICK:  # RIGHT CLICK
        #     if clicked_cell.cell_type == CellType.BLOCK:
        #         self.replace_cell(clicked_cell.cell, CellType.ICE, event)
    @log
    def handle_mouse_moving(self, clicked_cell: ClickedCell, event):
        """
        Handle mouse movement during cell dragging.

        Args:
            clicked_cell (ClickedCell): The ClickedCell representing the cell being dragged.
            click_type (int): The type of mouse click (LEFT_CLICK or RIGHT_CLICK).
            event (pygame.Event): The mouse event describing the movement.

        This method handles mouse movement events that occur while dragging a cell. It takes a
        ClickedCell object representing the dragged cell, the type of mouse click, and the mouse event
        that describes the movement.

        It updates the cell's position while dragging, and when the cell is moved over another cell,
        it checks the cell type and updates it based on the click type (LEFT_CLICK or RIGHT_CLICK).
        The method centralizes the logic for handling cell dragging and updating cell interactions.

        Parameters:
            clicked_cell (ClickedCell): The ClickedCell representing the cell being dragged.
            click_type (int): The type of mouse click (LEFT_CLICK or RIGHT_CLICK).
            event (pygame.Event): The mouse event describing the movement.
        """

        clicked_cell.handle_dragging(event) #check if it's a goal or a player, 

        updated_cell = self.update_current_cell(event) #updates the current gameboard cell you're working with

        if updated_cell:
            if self.click_type == LEFT_CLICK:
                self.replace_cell(updated_cell.cell, self.current_pallet_block, event)

            # elif self.click_type == RIGHT_CLICK:
            #         self.replace_cell(updated_cell.cell, CellType.ICE, event)
    @log
    def handle_mouse_up(self, clicked_cell: ClickedCell, event):
        """
        Handle mouse release event after dragging a cell.

        Args:
            clicked_cell (ClickedCell): The ClickedCell representing the cell that was dragged.
            click_type (int): The type of mouse click (LEFT_CLICK or RIGHT_CLICK).
            event (pygame.Event): The mouse event describing the release.

        This method handles the mouse release event that occurs after dragging a cell. It takes a
        ClickedCell object representing the dragged cell, the type of mouse click, and the mouse event
        that describes the release.

        It checks if the dragged cell was successfully moved during the dragging operation. If so,
        it updates cell positions and interactions based on the cell types and the position of the cell
        that is now underneath the dragged cell. After handling the interactions, it resets the editor's
        state and updates the gameboard.

        Parameters:
            clicked_cell (ClickedCell): The ClickedCell representing the cell that was dragged.
            click_type (int): The type of mouse click (LEFT_CLICK or RIGHT_CLICK).
            event (pygame.Event): The mouse event describing the release.
        """

        underneath_cell = self.update_current_cell(event, checkingUnderneath=True)
        underneath_goal = self.update_current_cell(event)

        if clicked_cell.is_draggable():
            clicked_cell.handle_dragging(event)
            self.update_cell_after_dragging(clicked_cell, underneath_cell, underneath_goal)

        self.reset_click()
    @log
    def update_current_cell(self, event: pygame.event.Event, checkingUnderneath: bool = False) -> pygame.sprite.Sprite:
        """
        Update the top-most clicked cell.

        This method iterates through the gameboard cells in reverse order (from top to bottom)
        to find the cell that collides with the given mouse event's position. The top-most
        cell is the last one that collides with the event's position. A ClickedCell object is
        created for the top cell, encapsulating its information, and returned.

        Args:
            event (pygame.event.Event): The mouse event containing the position of the click.
            checkingUnderneath (bool): Default False. 

        Returns:
            ClickedCell or None: The top-most clicked cell if found, or None if no cell
            collides with the event's position.
        """
        if not checkingUnderneath:
            for clicked_cell in reversed(list(self.gameboard_sprite_group)):
                if clicked_cell.rect.collidepoint(event.pos):
                    return  ClickedCell(clicked_cell, event)
            return None
                    
        else:
            for clicked_cell in (self.gameboard_sprite_group):
                if clicked_cell.rect.collidepoint(event.pos):
                    return ClickedCell(clicked_cell, event)
            return None
                    
    @log
    def check_for_pallet_click(self, event: pygame.event.Event):
        """
        Checks to see if any sprites in the block pallet have been clicked.

        If something in the pallet has been clicked, update the current_pallet_block property.

        """
        if self.block_pallet_sprite.rect.collidepoint(event.pos):
            self.current_pallet_block = CellType.BLOCK
            self.selected_pallet_sprite.rect.center = self.block_pallet_sprite.rect.center
        elif self.ice_pallet_sprite.rect.collidepoint(event.pos):
            self.current_pallet_block = CellType.ICE
            self.selected_pallet_sprite.rect.center = self.ice_pallet_sprite.rect.center
        print(self.current_pallet_block)
    @log
    def update(self, events: list[pygame.event.Event]):
        for event in events:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_type = event.button
                if event.button == LEFT_CLICK:
                    self.check_for_pallet_click(event)
                    self.clickedcell = self.update_current_cell(event)

                if self.clickedcell:
                    self.handle_mouse_click(self.clickedcell, event.button, event)
                

            elif event.type == pygame.MOUSEMOTION:
                if self.clickedcell:
                    self.handle_mouse_moving(self.clickedcell, event)
                                
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.clickedcell:
                    self.handle_mouse_up(self.clickedcell, event)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.level_manager.SaveInPlace(self.gameboard)
                    print("Saved in place.")
                elif event.key == pygame.K_s:
                    self.level_manager.SaveNew(self.gameboard)
                    print("Saved new map.")
    
    @log
    def draw_grid(self):
        """
        This is just temporary for showing the dimensions of the grid until we can start implementing sprites more regularly
        """
        border_size = Border_Size_Lookup[self.level_manager.current_difficulty]
        for x in range(border_size.width, WINDOW_DIMENSIONS.width-border_size.width + 1, CELL_DIMENSIONS.width):
            pygame.draw.line(self.screen, WHITE, (x, border_size.height), (x, WINDOW_DIMENSIONS.height-border_size.height))
        for y in range(border_size.height, WINDOW_DIMENSIONS.height-border_size.height + 1, CELL_DIMENSIONS.height):
            pygame.draw.line(self.screen, WHITE, (border_size.width, y), (WINDOW_DIMENSIONS.width-border_size.width, y))
    @log
    def draw(self):
        """
        Need to move the pallet sprite group into this class.

        In update check for collision with any of the pallet sprites.

        
        """
        self.pallete_sprite_group.update()
        self.pallete_sprite_group.draw(self.screen)
        self.draw_grid()

            