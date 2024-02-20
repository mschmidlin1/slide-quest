import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from modules.configs import TITLE_FONT, WINDOW_DIMENSIONS, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR, Border_Size_Lookup
from modules.Sprites import TextSprite, Player, Block, Ice, HollowSquareSprite
from modules.DataTypes import Point
from modules.GameEnums import GameDifficulty

class LevelBackground():
    def __init__(self, screen, text: str):
        
        self.screen = screen

        self.main_menu_sprite = TextSprite(
            "Press (Esc) for main menu", 
            TITLE_FONT, 
            15, 
            Point(10, 10),
            TITLE_SCREEN_TEXT_COLOR,
            anchor='topleft')

        self.current_level_sprite = TextSprite(
            f"{text}", 
            TITLE_FONT,
            15,
            Point(WINDOW_DIMENSIONS.width//2, 10),
            TITLE_SCREEN_TEXT_COLOR, 
            anchor='center')
        
        self.time_sprite = TextSprite(
            "", 
            TITLE_FONT,
            15,
            Point(WINDOW_DIMENSIONS.width-10, 10),
            TITLE_SCREEN_TEXT_COLOR,
            anchor='topright')
        
        self.solution_sprite = TextSprite(
            "",
            TITLE_FONT,
            15,
            Point(WINDOW_DIMENSIONS.width-10, WINDOW_DIMENSIONS.height-10),
            TITLE_SCREEN_TEXT_COLOR,
            anchor='bottomright')
        

        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.current_level_sprite)
        self.sprite_group.add(self.time_sprite)
        self.sprite_group.add(self.main_menu_sprite)
        self.sprite_group.add(self.solution_sprite)


        self.block_sprite = Block(Point(0, 0), Border_Size_Lookup[GameDifficulty.BEGINNER]) #the constructor arguments don't matter because we're gonna set the location manually
        self.block_sprite.rect.center = Point(60, WINDOW_DIMENSIONS.height-30)

        self.ice_sprite = Ice(Point(0, 0), Border_Size_Lookup[GameDifficulty.BEGINNER]) #the constructor arguments don't matter because we're gonna set the location manually
        self.ice_sprite.rect.center = Point(120, WINDOW_DIMENSIONS.height-30)

        self.hollow_rect_sprite = HollowSquareSprite(Point(60, WINDOW_DIMENSIONS.height-30), 4)

        self.pallete_sprite_group = pygame.sprite.Group()
        self.pallete_sprite_group.add(self.block_sprite)
        self.pallete_sprite_group.add(self.ice_sprite)
        self.pallete_sprite_group.add(self.hollow_rect_sprite)

    def draw(self, time_str: str, solution: str, edit_mode: bool = True):
        self.screen.fill(TITLE_SCREEN_COLOR)
        self.time_sprite.update_text(time_str)
        self.solution_sprite.update_text(solution)
        self.sprite_group.update()
        self.sprite_group.draw(self.screen)

        if edit_mode:
            self.pallete_sprite_group.update()
            self.pallete_sprite_group.draw(self.screen)




if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    clock = pygame.time.Clock()

    level_background = LevelBackground(screen, "This is the level name")

    while True:
        level_background.draw()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.flip()
        clock.tick(60)