import pygame
from modules.SQGame import SQGame
from modules.configs import WINDOW_WIDTH, WINDOW_HEIGHT
import sys

game = SQGame()

BLACK = (0, 0, 0)



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(title="Slide Quest")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()
        self.screen.fill(BLACK)


    while True:
        game.DrawBoard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
