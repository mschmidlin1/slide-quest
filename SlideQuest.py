import pygame
import sys
from modules.configs import *
from modules.sprites import *
from modules.GameBoard import *
from modules.GameEnums import *
from modules.Point import Point

class Game:
    """
    Basic initialization of pygame necessary variables
    """
    def __init__(self):
        self.gameboard = GameBoard(GAMEBOARD_DIMENSIONS)

        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

    def convert_digit_to_cell_type(self, char):
        try:
            char = int(char)
            if char in range(26):
                return CellType(char)
        except ValueError:
            pass
        return None

    def convert_line_to_strings(self, line):
        string_values = []
        for char in line.strip():
            cell_type = self.convert_digit_to_cell_type(char)
            if cell_type is not None:
                string_values.append(str(cell_type))
            else:
                print(f"Invalid digit: {char}")
        return string_values

    def new(self):
        """
        Creation of all sprites, this is needed to initlaize all sprites given their (x, y) values and passed a state of the game object
        This is run before the run function to make sure everything is initialized
        """

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.ice = pygame.sprite.LayeredUpdates()

        with open('levels\\beginner\\map.txt', 'r') as file:
            with open('levels\\beginner\\map.csv', 'w') as f:
                for line in file:
                    string_list = self.convert_line_to_strings(line)
                    string_str = ','.join(string_list) + '\n'
                    f.write(string_str)

        #implementation of GameBoard to initialize screen with all sprites from map csv
        for row, cells in enumerate(self.gameboard.ReadBoard('levels\\beginner\\map.csv')):
            for col, cell in enumerate(cells):
                if cell == 'CellType.BLOCK':
                    Wall(self, col, row)
                if cell == 'CellType.PLAYER':
                    self.player = Player(self, col, row)
                if cell == 'CellType.GOAL':
                    Goal(self, col, row)
                if cell == 'CellType.ICE':
                    Ice(self, col, row)

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
            if event.type == pygame.KEYDOWN:
                if event.key == Direction.LEFT.value and not self.player.moving:
                    self.player.set_target(self.gameboard.MovePlayer(Direction.LEFT))
                if event.key == Direction.RIGHT.value and not self.player.moving:
                    self.player.set_target(self.gameboard.MovePlayer(Direction.RIGHT))
                if event.key == Direction.UP.value and not self.player.moving:
                    self.player.set_target(self.gameboard.MovePlayer(Direction.UP))
                if event.key == Direction.DOWN.value and not self.player.moving:
                    self.player.set_target(self.gameboard.MovePlayer(Direction.DOWN))

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
        self.all_sprites.draw(self.screen)
        self.draw_grid()
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
        

if __name__=="__main__":
    g = Game()
    g.new()
    g.run()
