



import pygame
from sq_src.configs import ENVIRONMENT_SPRITE_SHEET, SPRITE_POSITIONS


class SpriteLoader:
    _sprites = {}

    @classmethod
    def load_sprite_sheet(cls):
        """
        Load and slice a sprite sheet.
        
        GLOBALS:
        - ENVIRONMENT_SPRITE_SHEET (str): Path to the sprite sheet file.
        - SPRITE_POSITIONS (dict): A dictionary with keys as sprite names and values as tuples
                                specifying the sprite's rectangle on the sprite sheet (x, y, width, height).
        

        """
        sprite_sheet = pygame.image.load(ENVIRONMENT_SPRITE_SHEET).convert_alpha()
        
        for sprite_name, pos in SPRITE_POSITIONS.items():
            x, y, width, height = pos
            sprite = sprite_sheet.subsurface((x, y, width, height))
            cls._sprites[sprite_name] = sprite

    @classmethod
    def get_sprite(cls, sprite_name: str) -> pygame.surface.Surface:
        """
        Retrieve a loaded sprite by name.
        
        Parameters:
        - sprite_name (str): The name of the sprite to retrieve.
        
        Returns:
        - pygame.Surface: The requested sprite.
        """
        return cls._sprites[sprite_name]