import pygame
from sq_src.configs import LEFT_CLICK, TITLE_FONT, DARK_GRAY, GRAY, WHITE
from sq_src.data_structures.data_types import Size, Point, Anchor
from sq_src.sprites.text_sprite import TextSprite

class Slider:
    def __init__(self, screen, initial_percent: float, center_pos: Point, slider_color, knob_color, slider_size: Size, knob_size: Size, font: str, font_size: int, label: str = '', knob_radius=2):
        """
        Initializes a new Slider object.

        Parameters:
        - screen: The pygame screen object where the slider will be drawn.
        - initial_percent (float): The initial position of the slider knob as a percentage (0 to 1).
        - center_pos (Point): The center position of the slider on the screen.
        - slider_color: The color of the slider track.
        - knob_color: The color of the slider knob.
        - slider_size (Size): The size (width and height) of the slider track.
        - knob_size (Size): The size (width and height) of the slider knob.
        - font (str): The file path to a font file.
        - font_size (int): The font size of the slider label.
        - label (str, optional): The text label displayed near the slider. Defaults to an empty string.

        The constructor initializes the slider's properties, calculates the position and size of the slider track and knob, and prepares the label and percentage display sprites.
        """
        self.screen = screen
        self.center_pos = center_pos
        self.slider_color = slider_color
        self.knob_color = knob_color
        self.slider_size = slider_size
        self.knob_size = knob_size
        self.label = label
        self.font_size = font_size
        self.knob_radius = knob_radius

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

        self.percent_label_loc = Point(self.slider_rect.right+24, self.slider_rect.top)
        self.percent_text_sprite = TextSprite(self.percent_str(), font, 28, self.percent_label_loc, self.knob_color, anchor=Anchor.CENTER)

        self.label_loc = Point(self.slider_rect.left, self.slider_rect.top-55)
        self.slider_label_sprite = TextSprite(label, font, self.font_size, self.label_loc, self.knob_color, anchor=Anchor.TOP_LEFT)

        self.mouse_offset = (0, 0)

        self.slider_sprite_group = pygame.sprite.Group()
        self.slider_sprite_group.add(self.percent_text_sprite)
        self.slider_sprite_group.add(self.slider_label_sprite)

    def percent_str(self) -> str:
        """
        Returns a string representation of the slider's current position as a whole number percentage (0-100).

        Returns:
        - A string representing the whole number percentage of the slider's current position.
        """
        return str(int(round(self.current_slider_percent*100)))


    def calculate_percent(self, x_px: int) -> float:
        """
        Determines the nearest pixel position for the middle of the knob based on a given percentage of the slider's length.

        Parameters:
        - percent (float): The target position of the slider as a percentage (0.0 to 1.0).

        Returns:
        - An integer representing the nearest pixel position for the middle of the knob.
        """
        percent_to_pixel = 1 / self.slider_size.width
        return percent_to_pixel * x_px

    def calculate_nearest_pixel_pos(self, percent: float) -> int:
        """
        Determines the nearest pixel position for the middle of the knob based on a given percentage of the slider's length.

        Parameters:
        - percent (float): The target position of the slider as a percentage (0.0 to 1.0).

        Returns:
        - An integer representing the nearest pixel position for the middle of the knob.
        """
        pixel_position = percent * self.slider_size.width
        return int(round(pixel_position))
    
    def is_over(self, pos) -> bool:
        """
        Checks if the given mouse position is over the slider's knob.

        Parameters:
        - pos: The mouse position as a tuple (x, y).

        Returns:
        - True if the mouse position is over the knob, False otherwise.
        """
        
        if self.knob_rect.left < pos[0] < self.knob_rect.right and self.knob_rect.top < pos[1] < self.knob_rect.bottom:
            return True
        else:
            return False


    def draw(self):
        """
        Draws the slider (track and knob) and its associated text (label and percentage) on the screen.
        This method should be called within the game loop to render the slider.
        """

        pygame.draw.rect(self.screen, self.slider_color, self.slider_rect)
        pygame.draw.rect(self.screen, self.knob_color, self.knob_rect, border_radius=self.knob_radius)
        self.slider_sprite_group.draw(self.screen)

    def update(self, events: list[pygame.event.Event]):
        """
        Updates the slider's position and appearance based on user interaction and provided events.

        Parameters:
        - events (list[pygame.event.Event]): A list of pygame events to process, typically passed from the event loop.

        This method processes mouse button presses, movements, and releases to enable dragging of the slider knob.
        It also updates the slider's percentage display in real time as the knob is moved.
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


        