import pygame
import sys
from modules.Game import Game
from modules.configs import WINDOW_DIMENSIONS, WINDOW_TITLE, TITLE_FONT, TITLE_SCREEN_COLOR, TITLE_SCREEN_TEXT_COLOR, PLAYER_COLOR
from modules.Point import Point


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text_surface: pygame.Surface, center_location: Point):
        super().__init__()
        self.image = text_surface
        self.rect = self.image.get_rect()
        self.rect.center = center_location

class TitleScreenPlayerSprite(pygame.sprite.Sprite):
    def __init__(self, center_location: Point):
        super().__init__()
        self.surface = pygame.Surface((100, 100))
        self.surface.fill(PLAYER_COLOR)
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.center = center_location

if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(TITLE_FONT, 100)
    spacebar_font = pygame.font.Font(TITLE_FONT, 40)

    startup_surface = pygame.Surface(WINDOW_DIMENSIONS)
    startup_surface.fill(TITLE_SCREEN_COLOR)
    title_surface = title_font.render("Slide Quest!", True, TITLE_SCREEN_TEXT_COLOR)
    spacebar_text_surface = spacebar_font.render("Press Space to start!", True, TITLE_SCREEN_TEXT_COLOR)

    title_sprite = TextSprite(title_surface, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//5))
    spacebar_sprite = TextSprite(spacebar_text_surface, Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1] - WINDOW_DIMENSIONS[1]//4))

    title_screen_sprites = pygame.sprite.Group()
    title_screen_sprites.add(title_sprite)
    title_screen_sprites.add(TitleScreenPlayerSprite(Point(WINDOW_DIMENSIONS[0]//2, WINDOW_DIMENSIONS[1]//2)))
    title_screen_sprites.add(spacebar_sprite)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        screen.blit(startup_surface, (0,0))
        title_screen_sprites.update()
        title_screen_sprites.draw(screen)

        pygame.display.update()
        clock.tick(60)







    # g = Game()
    # g.new()
    # g.run()
