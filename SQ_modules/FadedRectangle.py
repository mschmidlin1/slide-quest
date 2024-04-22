import pygame
from SQ_modules.DataTypes import Point, Size

class FadedRectangle:
    """
    This class represents a rectangle with a fading effect around the edges.

    Attributes:
        screen (pygame.surface.Surface): The pygame Surface object to draw the rectangle on.
        center (Point): The center point of the rectangle.
        size (Size): The size of the rectangle (width and height).
        color (tuple): The color of the rectangle (RGB values).
        fade_distance (int): The distance from the edge of the rectangle where the fading starts (default: 20).
    """
    def __init__(self, screen: pygame.surface.Surface, center: Point, size: Size, color, fade_distance=20):
        """
        Initializes a new FadedRectangle object.

        Args:
            screen (pygame.surface.Surface): The pygame Surface object to draw the rectangle on.
            center (Point): The center point of the rectangle.
            size (Size): The size of the rectangle (width and height).
            color (tuple): The color of the rectangle (RGB values).
            fade_distance (int, optional): The distance from the edge of the rectangle where the fading starts (default: 20).
        """
        self.screen = screen
        self.center = center
        self.size = size
        self.color = color
        self.fade_distance = fade_distance
        self.left = center.x - (size.width // 2)
        self.top = center.y - (size.height // 2)
        self.ellipse_rect = pygame.Rect(self.left, self.top, self.size.width, self.size.height)
        self.gradient_surface = self.create_gradient_surface()

    def create_gradient_surface(self):
        """
        Creates a temporary surface with a gradient applied, used for drawing the faded rectangle.

        This method is called only once during initialization to improve performance.

        Returns:
            pygame.Surface: A new surface with the gradient applied.
        """
        temp_surface = pygame.Surface((self.ellipse_rect.width, self.ellipse_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, self.color + (255,), [0, 0, self.ellipse_rect.width, self.ellipse_rect.height])
        
        # Create gradient only once
        for x in range(self.ellipse_rect.width):
            for y in range(self.ellipse_rect.height):
                distance_x = min(x, self.ellipse_rect.width - x - 1)
                distance_y = min(y, self.ellipse_rect.height - y - 1)
                distance = min(distance_x, distance_y)
                alpha = max(0, min(255, int(255 * (distance / self.fade_distance))))
                if distance <= self.fade_distance:
                    current_color = temp_surface.get_at((x, y))
                    temp_surface.set_at((x, y), current_color[:-1] + (alpha,))

        return temp_surface

    def draw(self):
        """
        Draws the FadedRectangle onto the specified screen surface.
        """
        self.screen.blit(self.gradient_surface, (self.ellipse_rect.x, self.ellipse_rect.y))

