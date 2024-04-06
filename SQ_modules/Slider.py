import pygame
from SQ_modules.configs import LEFT_CLICK, GAME_VOLUME, TITLE_FONT
from SQ_modules.DataTypes import Size, Point
from SQ_modules.Sprites import TextSprite

class Slider:
    def __init__(self, screen, initial_percent: float, center_pos: Point, slider_color, knob_color, slider_size: Size, knob_size: Size, font: str, label: str = ''):
        """
        x and y are the top left corner
        """
        self.screen = screen
        self.center_pos = center_pos
        self.slider_color = slider_color
        self.knob_color = knob_color
        self.slider_size = slider_size
        self.knob_size = knob_size
        self.label = label

        self.dragging = False

        self.current_slider_percent = initial_percent

        top_left = (self.center_pos.x - (self.slider_size.width//2), self.center_pos.y - (self.slider_size.height//2))
        width_height = (self.slider_size.width, self.slider_size.height)
        self.slider_rect = pygame.Rect(top_left, width_height)

        center_x = self.calculate_nearest_pixel_pos(self.current_slider_percent) + self.slider_rect.left
        left_x = center_x-(self.knob_size.width//2)

        top_left = (left_x, self.center_pos.y - (self.knob_size.height//2))
        width_height = (self.knob_size.width, self.knob_size.height)
        self.knob_rect = pygame.Rect(top_left, width_height)

        self.percent_label_loc = Point(self.slider_rect.right+20, self.slider_rect.top)
        self.percent_text_sprite = TextSprite(self.percent_str(), font, 20, self.percent_label_loc, self.knob_color, anchor='center')

        self.label_loc = Point(self.slider_rect.left, self.slider_rect.top-40)
        self.slider_label_sprite = TextSprite(label, font, 40, self.label_loc, self.knob_color, anchor='topleft')

        self.mouse_offset = (0, 0)

        self.slider_sprite_group = pygame.sprite.Group()
        self.slider_sprite_group.add(self.percent_text_sprite)
        self.slider_sprite_group.add(self.slider_label_sprite)

    def percent_str(self) -> str:
        """
        Uses the current slider percent and returns a whole number percent 0-100 of where the slider currently is.
        """
        return str(int(round(self.current_slider_percent*100)))


    def calculate_percent(self, x_px: int) -> float:
        """
        Takes in a pixel distance (relative to the start of the slider) and returns the percentage as a float [0-1]
        """
        percent_to_pixel = 1 / self.slider_size.width
        return percent_to_pixel * x_px

    def calculate_nearest_pixel_pos(self, percent: float) -> int:
        """
        Takes in a percentage of the slider and returns the pixel position of the middle of the knob to the nearest pixel.
        """
        pixel_position = percent * self.slider_size.width
        return int(round(pixel_position))
    
    def is_over(self, pos) -> bool:
        """
        Checks if a mouse potition (pos) is over the button
        """
        
        if self.knob_rect.left < pos[0] < self.knob_rect.right and self.knob_rect.top < pos[1] < self.knob_rect.bottom:
            return True
        else:
            return False


    def draw(self):
        """
        Call this method to draw the button on the screen
        """

        pygame.draw.rect(self.screen, self.slider_color, self.slider_rect)
        pygame.draw.rect(self.screen, self.knob_color, self.knob_rect)
        self.slider_sprite_group.draw(self.screen)

    def update(self, events: list[pygame.event.Event]):
        """
        
        """
        self.percent_text_sprite.update_text(self.percent_str())
        self.percent_text_sprite.update()


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    if self.is_over(event.pos):
                        self.dragging = True
                        self.mouse_offset = event.pos[0]-self.knob_rect.centerx
            if event.type == pygame.MOUSEMOTION:
                if self.dragging == True:
                    new_x = event.pos[0] - self.mouse_offset
                    #make sure the new position is inside the slider
                    new_x = max(new_x, self.slider_rect.left)
                    new_x = min(new_x, self.slider_rect.right)
                    self.current_slider_percent = self.calculate_percent(new_x - self.slider_rect.left)
                    move_distance = new_x - self.knob_rect.centerx
                    self.knob_rect.move_ip(move_distance, 0)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == LEFT_CLICK:
                    self.dragging = False
                    self.mouse_offset = 0


        