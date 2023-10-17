import pygame
from modules.SQGame import SQGame
from modules.configs import WINDOW_WIDTH, WINDOW_HEIGHT
import sys

game = SQGame()

BLACK = (0, 0, 0)

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
SCREEN.fill(BLACK)


while True:
    game.DrawBoard()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
