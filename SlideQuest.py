import pygame
from modules.configs import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        #load map
        pass

    def new(self):
        #initialization of all variables for new games
        pass


    def run(self):
        #game loop - set self.playing to False to end game

        self.playing = True

        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_WIDTH):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_HEIGHT):
            pygame.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        pygame.display.flip()


    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        pass

g = Game()

while True:
    g.new()
    g.run()
