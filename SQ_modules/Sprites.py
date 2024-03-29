import pygame
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SQ_modules.GameEnums import CellType, GameDifficulty
from SQ_modules.configs import CELL_DIMENSIONS, WALL_COLOR, GOAL_COLOR, GROUND_COLOR, ICE_COLOR, PLAYER_COLOR, PLAYER_SPEED, PALLET_HIGHLIGHT_COLOR, SELECTOR_TOOL_IMAGE, Border_Size_Lookup, PLAYER_SPRITE_SHEET, PLAYERSHADOW_SPRITE_SHEET, ENVIRONMENT_SPRITE_SHEET 
from SQ_modules.DataTypes import Point, Size, Cell
from SQ_modules.my_logging import set_logger, log
from SQ_modules.Converters import PointToCell, CellToPoint
import logging

class SpriteLoader:
    _sprites = {}

    @classmethod
    def load_sprite_sheet(cls, sheet_path, sprite_positions):
        """
        Load and slice a sprite sheet.
        
        Parameters:
        - sheet_path (str): Path to the sprite sheet file.
        - sprite_positions (dict): A dictionary with keys as sprite names and values as tuples
                                specifying the sprite's rectangle on the sprite sheet (x, y, width, height).
        
        Returns:
        - dict: A dictionary of sprite names and their corresponding pygame.Surface objects.
        """
        sprite_sheet = pygame.image.load(sheet_path).convert_alpha()
        
        for sprite_name, pos in sprite_positions.items():
            x, y, width, height = pos
            sprite = sprite_sheet.subsurface((x, y, width, height))
            cls._sprites[sprite_name] = sprite

    @classmethod
    def get_sprite(cls, sprite_name):
        """
        Retrieve a loaded sprite by name.
        
        Parameters:
        - sprite_name (str): The name of the sprite to retrieve.
        
        Returns:
        - pygame.Surface: The requested sprite.
        """
        return cls._sprites.get(sprite_name)

    @classmethod
    def get_ice_sprite(cls):
        return cls.load_sprite(ENVIRONMENT_SPRITE_SHEET, (32, 224, 32, 32))

    @classmethod
    def get_block_sprite(cls):
        return cls.load_sprite(ENVIRONMENT_SPRITE_SHEET, (32, 352, 32, 32))

    @classmethod
    def get_goal_sprite(cls):
        return cls.load_sprite(ENVIRONMENT_SPRITE_SHEET, (64, 256, 32, 32))


class Player(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.PLAYER
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.sprite_size = (50, 37)  # The size of a single sprite
        self.setup_sprites()  # Setup sprite imaging
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)
        self.current_pos = self.rect.center
        self.moving = False
        self.speed = PLAYER_SPEED
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 600  # Milliseconds per frame

    def setup_sprites(self):
        """
        Loads the sprite sheet, slices it into frames, and sets the initial sprite image.
        """
        self.sprite_sheet = pygame.image.load(PLAYER_SPRITE_SHEET).convert_alpha()  # Load the sprite sheet
        self.shadow_sprite = pygame.image.load(PLAYERSHADOW_SPRITE_SHEET).convert_alpha()  # Load the sprite sheet

        self.shadow_sprite = pygame.transform.scale(self.shadow_sprite, (32, 32))

        self.idle_frames = self.load_frames(4)  # Load the first four frames for idle animation
        self.current_frame = 0
        self.image = self.idle_frames[self.current_frame]  # Start with the first frame

    def load_frames(self, number_of_frames: int):
        """
        Slices the sprite sheet into individual frames.
        """
        frames = []
        for i in range(number_of_frames):
            frame = self.sprite_sheet.subsurface((i * self.sprite_size[0], 0, self.sprite_size[0], self.sprite_size[1]))
            frames.append(frame)
        return frames

    def update_sprite(self):
        """
        Update the sprite image based on the player's state. For example, cycle through
        idle frames or switch to a moving animation.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame]

    def draw_player(self, screen):
        """
        Custom drawing of the player sprite to control its visual representation.
        """
        # Custom drawing logic (for example, aligning the bottom middle of the sprite)
        image_bottom_middle = (self.rect.centerx - self.image.get_width() / 2,
                               self.rect.centery - self.image.get_height())
        
        # Calculate the position for the shadow sprite
        # Assuming the shadow should be centered directly under the player sprite
        shadow_pos = (self.rect.centerx - self.shadow_sprite.get_width() / 2,
                    (self.rect.centery - 3) - self.shadow_sprite.get_height() / 2)

        # Blit the shadow sprite first
        screen.blit(self.shadow_sprite, shadow_pos)
        screen.blit(self.image, image_bottom_middle)

    def move(self, location: Cell):
        """
        Set's the target position for the player as long as the player is not already moving.
        """
        self.current_pos_cell = PointToCell(Point(self.rect.center[0], self.rect.center[1]), self.difficulty)

        #target and current position in Cell gameboard coordinates, but needs to be in x,y order        
        self.current_pos = pygame.Vector2((self.current_pos_cell.col, self.current_pos_cell.row))
        self.target_pos_cell = location
        self.target_pos = pygame.Vector2(location.col, location.row)

        logging.info(f"Starting Position:  {self.current_pos_cell}  Target Position:  {self.target_pos_cell}")

        self.moving = True

    def update(self):

        current_time = pygame.time.get_ticks()

        if self.moving:
            
            self.target_pos_pixels = CellToPoint(self.target_pos_cell, self.difficulty)

            if self.rect.center == self.target_pos_pixels:
                self.moving = False
                return
            
            distance_to_target = self.target_pos - self.current_pos
            distance_to_target_length = distance_to_target.length()
            
            if distance_to_target_length < self.speed:
                self.rect.center = self.target_pos_pixels
                self.moving = False
                return
            
            if distance_to_target_length != 0:
                distance_to_target.normalize_ip()
                distance_to_target = distance_to_target * PLAYER_SPEED
                self.current_pos += distance_to_target

            #have to do manual conversion until I think of a better way to structure the converter.
            x = Border_Size_Lookup[self.difficulty].width + (self.current_pos[0] * CELL_DIMENSIONS.width) + (CELL_DIMENSIONS.width // 2)
            y = Border_Size_Lookup[self.difficulty].height + (self.current_pos[1] * CELL_DIMENSIONS.height) + (CELL_DIMENSIONS.height // 2)
            self.rect.center = Point(round(x), round(y))

        else:
            # Update the frame if it's time            
            if current_time - self.last_update > self.frame_rate:
                self.last_update = current_time
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_frame]

class Block(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.BLOCK
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        block_variants = ['block_1x1_a', 'block_1x1_b', 'block_1x1_c', 'block_1x1_d', 'block_1x1_e']
        chosen_block = random.choice(block_variants)  
        self.image = SpriteLoader.get_sprite(chosen_block)  # Use the chosen sprite
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class Ground(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.GROUND
        self.difficulty = difficulty
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS)
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)


class Goal(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.GOAL
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.image = SpriteLoader.get_sprite('goal')
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class Ice(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.ICE
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.image = SpriteLoader.get_sprite('ice')
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class Border(pygame.sprite.Sprite):
    def __init__(self, position: Point, sprite_name: str):
        super().__init__()
        self.image = SpriteLoader.get_sprite(sprite_name)
        self.rect = self.image.get_rect()
        self.rect.topleft = (position.x, position.y)

class Background(pygame.sprite.Sprite):
    def __init__(self, position: Point):
        super().__init__()
        self.image = SpriteLoader.get_sprite('background')
        self.rect = self.image.get_rect()
        self.rect.topleft = (position.x, position.y)

class Highlighter(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = "Highlighter"
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self._layer = 0
        self.gameboard_loc = gameboard_loc
        self.image = pygame.Surface(CELL_DIMENSIONS, pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 128))
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)

class SelectorTool(pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__()
        self.image = SELECTOR_TOOL_IMAGE
        self.rect = self.image.get_rect()

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text: str, font_file: str, font_size: int, location: Point, color: tuple = (0,0,0), anchor: str = 'center', outline_color: tuple = None, outline_width: int = 2):
        super().__init__()
        self.font = pygame.font.Font(font_file, font_size)
        self.color = color
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.anchor = anchor
        self.location = location
        self.update_text(text)
        
    def render_text_with_outline(self, text: str):
        # Render the base text
        base_text = self.font.render(text, True, self.color)
        if not self.outline_color:
            return base_text
        
        # Create a surface to hold the text with an outline
        outline_surface = pygame.Surface(base_text.get_rect().inflate(self.outline_width*2, self.outline_width*2).size, pygame.SRCALPHA)
        
        # Render the outline by blitting the base text multiple times with an offset
        outline_rect = base_text.get_rect()
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # You can add more directions for a thicker outline
            outline_surface.blit(self.font.render(text, True, self.outline_color), (outline_rect.x + dx*self.outline_width, outline_rect.y + dy*self.outline_width))
        
        # Blit the base text onto the outline surface
        outline_surface.blit(base_text, (self.outline_width, self.outline_width))
        return outline_surface

        
    def update_text(self, text: str):
        self.image = self.render_text_with_outline(text)
        self.rect = self.image.get_rect()
        if self.anchor == 'center':
            self.rect.center = self.location
        elif self.anchor == 'topleft':
            self.rect.topleft = self.location
        elif self.anchor == 'topright':
            self.rect.topright = self.location
        elif self.anchor == 'bottomleft':
            self.rect.bottomleft = self.location
        elif self.anchor == 'bottomright':
            self.rect.bottomright = self.location
        else:
            raise ValueError("Invalid anchor point")

# class TitleScreenPlayerSprite(pygame.sprite.Sprite):
#     def __init__(self, center_location: Point):
#         super().__init__()
#         self.surface = pygame.Surface((100, 100))
#         self.surface.fill(PLAYER_COLOR)
#         self.image = self.surface
#         self.rect = self.image.get_rect()
#         self.rect.center = center_location

class HollowSquareSprite(pygame.sprite.Sprite):
    def __init__(self, location: Point, thickness: int, color=PALLET_HIGHLIGHT_COLOR, transparent_color=(0, 0, 0, 0)):
        super().__init__()
        
        # Create a transparent surface with the given size
        self.image = pygame.Surface((CELL_DIMENSIONS[0]+thickness, CELL_DIMENSIONS[1]+thickness), pygame.SRCALPHA)
        
        # Draw the outer square
        pygame.draw.rect(self.image, color, self.image.get_rect(), thickness)
        
        # Draw the inner transparent square
        inner_rect = pygame.Rect(thickness, thickness, CELL_DIMENSIONS[0]//2, CELL_DIMENSIONS[1]//2)
        pygame.draw.rect(self.image, transparent_color, inner_rect)
        
        self.rect = self.image.get_rect()

        self.rect.center = location



def FindSpritesByLocation(sprite_group: pygame.sprite.Group, location: Cell) -> list[pygame.sprite.Sprite]:
    """
    Retrieves a list of sprites from a specified sprite group where each sprite has the specific `location` on the game board.

    If a sprite does not have the `gameboard_loc` attribute, it is ignored. Only sprites whose 'gameboard_loc' matches the specified location are included in the result.

    The function returns an empty list if no sprites are found at the specified location.

    Parameters:
    -
    - sprite_group (pygame.sprite.Group): The group of sprites to search through.
    - location (Cell): The location on the game board for which to find sprites.

    Returns:
    -
    - list[pygame.sprite.Sprite]: A list of sprites from the given sprite group that are located at `location` on the game board.

    Example:
    -
    ```
    found_sprites = GetSpriteByLocation(game_sprites, desired_location)
    for sprite in found_sprites:
        print(sprite)
    ```
    """
    sprites = []
    for sprite in sprite_group:
        if not hasattr(sprite, 'gameboard_loc'):
            continue
        if sprite.gameboard_loc == location:
            sprites.append(sprite)
    return sprites