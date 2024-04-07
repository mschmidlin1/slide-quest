import pygame
from SQ_modules.Sprites import TextSprite
from SQ_modules.DataTypes import Point

class Button:
    def __init__(self, screen, color, center_pos: Point, width, height, font_file: str, font_size: int, text='', font_color=(0, 0, 0), outline_color=None, hover_color=None, font=None):
        """
        
        """
        self.screen = screen
        self.color = color
        self.color_copy = color
        self.center_pos = center_pos
        self.width = width
        self.height = height
        self.top_left = Point(self.center_pos.x - (self.width // 2), self.center_pos.y - (self.height // 2))
        self.text = text
        self.outline_color = outline_color
        self.hover_color = hover_color
        self.font_file = font_file
        self.font_size = font_size
        self.font_color = font_color
        if self.hover_color is None:
            self.hover_color = self.color


        self.label = TextSprite(text, self.font_file, self.font_size, center_pos, self.font_color, anchor='center')

        self.label_sprite_group = pygame.sprite.Group()
        self.label_sprite_group.add(self.label)
        # self.font = font
        # if self.font is None:
        #     self.font = font = pygame.font.SysFont('comicsans', 60)


    def is_over(self, pos) -> bool:
        """
        Checks if a mouse potition (pos) is over the button
        """
        if self.top_left.x < pos[0] < self.top_left.x + self.width and self.top_left.y < pos[1] < self.top_left.y + self.height:
            return True
        else:
            return False


    def draw(self):
        """
        Call this method to draw the button on the screen
        """
        if self.outline_color:
            pygame.draw.rect(self.screen, self.outline_color, (self.top_left.x-2, self.top_left.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(self.screen, self.color, (self.top_left.x, self.top_left.y, self.width, self.height), 0)
        

        self.label_sprite_group.draw(self.screen)
        # if self.text != '':
        #     text = self.font.render(self.text, 1, (0,0,0))
        #     self.screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

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

        
    