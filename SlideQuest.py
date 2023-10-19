import pygame
from modules.configs import *
from modules.sprites import *
import sys

class Game:
    """
    Basic initialization of pygame necessary variables
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()


    def load_data(self):
        """
        load map --- this is where we can implement a text file with the exact desgn we want
        """
        pass

    
    def new(self):
        """
        Creation of all sprites, this is needed to initlaize all sprites given their (x, y) values and passed a state of the game object
        This is run before the run function to make sure everything is initialized
        """
        #initialization of all variables for new games
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self, 0, 0)
        pass

    
    def run(self):
        """
        This is the main function for running all other events, updates and draw calls this is called within the main while loop
        """
        
        self.playing = True
        #game loop - set self.playing to False to end game

        while self.playing:
            self.events()
            self.update()
            self.draw()

    
    def events(self):
        """
        This is where we can implement player movement as well as menu interactions such as starting the game or quiting 
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    
    def draw_grid(self):
        """
        This is just temporary for showing the dimensions of the grid until we can start implementing sprites more regularly
        """
        for x in range(0, WINDOW_WIDTH, CELL_WIDTH):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_HEIGHT):
            pygame.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        """
        Draw the sprite groups to the screen as well as handle the screen updating (pygame.display.flip())
        """
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        #this is for updating the entire sceen instead of pygame.display.update which only updates a portion
        pygame.display.flip()


    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        """
        updating sprites specifically (moreso for movement) and will handle player screen camera movement 
        if we want to implement procedural generation like lunatics
        """
        self.all_sprites.update()

g = Game()

while True:
    g.new()
    g.run()
