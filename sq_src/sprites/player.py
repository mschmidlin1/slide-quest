




import pygame

from sq_src.configs import CELL_DIMENSIONS, PLAYER_SPEED, PLAYER_SPRITE_SHEET, Border_Size_Lookup
from sq_src.data_structures.converters import CellToPoint, PointToCell
from sq_src.data_structures.data_types import Cell, Point
from sq_src.data_structures.game_enums import CellType, GameDifficulty
from sq_src.singletons.my_logging import LoggingService


class Player(pygame.sprite.Sprite):
    def __init__(self, gameboard_loc: Cell, difficulty: GameDifficulty):
        super().__init__()
        self.cellType = CellType.PLAYER
        self.difficulty = difficulty
        self.border_size = Border_Size_Lookup[difficulty]
        self.gameboard_loc = gameboard_loc
        self.sprite_size = (32, 32)  # The size of a single sprite
        self.setup_sprites()  # Setup sprite imaging
        self.rect = self.image.get_rect()
        self.rect.center = CellToPoint(gameboard_loc, self.difficulty)
        self.current_pos = self.rect.center
        self.moving = False
        self.speed = PLAYER_SPEED
        self.last_direction = "DOWN"  # A default direction
        self.current_type = 'ice'
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0  # Reset frame index
        self.frame_rate = 300  # Milliseconds per frame
        self.update_shadow_position()
        self.logging_service = LoggingService()

    def setup_sprites(self):
        """
        Loads the sprite sheet, slices it into frames, and sets the initial sprite image.
        """
        self.sprite_sheet = pygame.image.load(PLAYER_SPRITE_SHEET).convert_alpha()  # Load the sprite sheet
        self.shadow_sprite = self.sprite_sheet.subsurface((352, 140, self.sprite_size[0] / 2, self.sprite_size[1])) #magic numbers until I can annotate them better

        # Load frame sets for each direction

        #idle
        self.idle_front_frames = self.load_frames(3, 64, 140)
        self.idle_back_frames = self.load_frames(3, 0, 140)
        self.idle_side_frames = self.load_frames(3, 32, 140)

        #celebrate
        self.celebrate_frames = self.load_frames(8, 64, 24)

        #ground walking
        self.mvmt_up_grnd_frames = self.load_frames(8, 0, 24)
        self.mvmt_down_grnd_frames = self.load_frames(8, 64, 0)
        self.mvmt_side_grnd_frames = self.load_frames(8, 32, 24)

        #ice sliding
        self.mvmt_up_ice_frames = self.load_frames(8, 0, 24)
        self.mvmt_down_ice_frames = self.load_frames(8, 96, 0)
        self.mvmt_side_ice_frames = self.load_frames(8, 32, 24)

        # Organize animations by action and direction
        self.animations = {
            'idle': {
                'UP': self.idle_back_frames,
                'DOWN': self.idle_front_frames,
                'SIDE': self.idle_side_frames,
            },
            'celebrate': {
                'DOWN': self.celebrate_frames
            },
            'ground': {
                'UP': self.mvmt_up_grnd_frames,
                'DOWN': self.mvmt_down_grnd_frames,
                'SIDE': self.mvmt_side_grnd_frames,
            },
            'ice': {
                'UP': self.mvmt_up_ice_frames,
                'DOWN': self.mvmt_down_ice_frames,
                'SIDE': self.mvmt_side_ice_frames,
            }
        }

        # Initialize with a default state and direction
        self.current_type = 'idle'
        self.current_direction = 'DOWN'

        # Select the initial set of frames based on the current state and direction
        self.current_frames = self.animations[self.current_type][self.current_direction]
        self.current_frame = 0
        self.image = self.current_frames[self.current_frame]
    
    def get_directional_frames(self, direction):
        if self.state == "idle":

            direction_key = direction if direction in ['UP', 'DOWN'] else 'SIDE'
            frames = self.animations['idle'][direction_key]

            if direction == 'LEFT':
                frames = [pygame.transform.flip(frame, True, False) for frame in frames]

        elif self.state == "moving":
            # For movement states (e.g., 'ground', 'ice'), handle LEFT and RIGHT by flipping SIDE frames for LEFT.
            if direction in ['LEFT', 'RIGHT']:
                frames = self.animations[self.current_type]['SIDE']
                if direction == 'LEFT':
                    frames = [pygame.transform.flip(frame, True, False) for frame in frames]
            else:
                frames = self.animations[self.current_type][direction]

        return frames

    def change_direction(self, direction):
        self.last_direction = direction
        self.current_frame = 0  # Reset frame index
        self.current_frames = self.get_directional_frames(direction)
        self.image = self.current_frames[self.current_frame]  # Update the sprite image

    def load_frames(self, number_of_frames: int, x_start = 0, y_start= 0):
        """
        Slices the sprite sheet into individual frames.
        """
        frames = []
        frame_width, frame_height = self.sprite_size

        x_offset = 128
        gap = 32  # The gap between lines of sprites
        rows = 2  # Number of rows to alternate between

        if number_of_frames == 3:

            for i in range(number_of_frames):
                current_x = x_start + i * x_offset
                frame = self.sprite_sheet.subsurface((current_x, y_start, self.sprite_size[0], self.sprite_size[1]))
                frames.append(frame)

            return frames
        
        if number_of_frames == 8:

            for i in range(number_of_frames):
                row = (i % rows)  # Alternate rows
                column = (i // rows)  # Move to the next column after completing each row

                current_x = x_start + column * x_offset
                current_y = y_start + row * (frame_height + gap)

                frame = self.sprite_sheet.subsurface((current_x, current_y, frame_width, frame_height))
                frames.append(frame)

            return frames

    def update_sprite(self):
        """
        Update the sprite image based on the player's state. This method now dynamically selects the correct
        frame set to cycle through based on the player's current action and direction, stored in self.current_frames.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            # Cycle through the current frame set
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            self.image = self.current_frames[self.current_frame]

    def update_shadow_position(self):
        shadow_offset_x = 0
        shadow_offset_y = 4
        
        # Update the shadow position
        shadow_pos = (self.rect.centerx + shadow_offset_x - self.shadow_sprite.get_width() / 2,
                    self.rect.centery + shadow_offset_y - self.shadow_sprite.get_height() / 2)

        self.shadow_pos = shadow_pos

    def draw_player(self, screen):
        # Draw the shadow first using the updated position
        if self.current_type != 'celebrate':
            screen.blit(self.shadow_sprite, self.shadow_pos)
        
        # Then draw the player sprite
        image_position = (self.rect.centerx - self.image.get_width() / 2,
                      self.rect.centery - self.image.get_height() / 2)

        screen.blit(self.image, self.rect)

    def move(self, location: Cell, direction):
        """
        Set's the target position for the player as long as the player is not already moving.
        """
        self.last_direction = direction
        self.change_direction(direction)

        self.current_pos_cell = PointToCell(Point(self.rect.center[0], self.rect.center[1]), self.difficulty)

        #target and current position in Cell gameboard coordinates, but needs to be in x,y order        
        self.current_pos = pygame.Vector2((self.current_pos_cell.col, self.current_pos_cell.row))
        self.target_pos_cell = location
        self.target_pos = pygame.Vector2(location.col, location.row)
        self.logging_service.log_debug(f"Starting Position:  {self.current_pos_cell}  Target Position:  {self.target_pos_cell}")

        self.moving = True

    def update(self):
        current_time = pygame.time.get_ticks()

        # Movement logic remains the same
        if self.moving:
            self.state = "moving"
            self.current_frames = self.get_directional_frames(self.last_direction)

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
                distance_to_target *= PLAYER_SPEED
                self.current_pos += distance_to_target

            x = Border_Size_Lookup[self.difficulty].width + (self.current_pos[0] * CELL_DIMENSIONS.width) + (CELL_DIMENSIONS.width // 2)
            y = Border_Size_Lookup[self.difficulty].height + (self.current_pos[1] * CELL_DIMENSIONS.height) + (CELL_DIMENSIONS.height // 2)
            self.rect.center = Point(round(x), round(y))
            self.update_shadow_position()

        else:
            if self.current_type == 'celebrate':
                self.current_frames = self.get_directional_frames(self.last_direction)
            else:
                self.state = "idle"
                self.current_frames = self.get_directional_frames(self.last_direction)

        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            self.current_frame += 1
            self.current_frame %= len(self.current_frames)
            self.image = self.current_frames[self.current_frame]
