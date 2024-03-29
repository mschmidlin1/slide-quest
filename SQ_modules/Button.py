import pygame

class Button:
    def __init__(self, screen, color, x, y, width, height, text='', outline_color=None, hover_color=None, font=None):
        """
        x and y are the top left corner
        """
        self.screen = screen
        self.color = color
        self.color_copy = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.outline_color = outline_color
        self.hover_color = hover_color
        if self.hover_color is None:
            self.hover_color = self.color

        self.font = font
        if self.font is None:
            self.font = font = pygame.font.SysFont('comicsans', 60)


    def is_over(self, pos) -> bool:
        """
        Checks if a mouse potition (pos) is over the button
        """
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        else:
            return False


    def draw(self):
        """
        Call this method to draw the button on the screen
        """
        if self.outline_color:
            pygame.draw.rect(self.screen, self.outline_color, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            text = self.font.render(self.text, 1, (0,0,0))
            self.screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def update(self, events: list[pygame.event.Event]):
        """
        
        """
        pos = None
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos

        if pos is None:#this probably shouldn't happen
            return


        if self.is_over(pos):
            self.color = self.hover_color
        else:
            self.color = self.color_copy

        
    