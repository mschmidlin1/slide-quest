import pygame
from modules.configs import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_WIDTH, CELL_HEIGHT

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

CLOCK = pygame.time.Clock()
WHITE = (255, 255, 255)
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class SQGame:
    def __init__(self): #initial variables specifically for the creation of the grid (add more later)
        pass 

    def DrawBoard(self):
        CELL_DIMS = 32

        for x in range(0, WINDOW_WIDTH, CELL_WIDTH):
            for y in range(0, WINDOW_HEIGHT, CELL_HEIGHT):
                rect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(SCREEN, WHITE, rect, 1)