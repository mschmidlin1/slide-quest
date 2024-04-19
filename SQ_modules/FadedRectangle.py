import pygame
from SQ_modules.DataTypes import Point, Size

class FadedRectangle:
    def __init__(self, screen: pygame.surface.Surface, center: Point, size: Size, color, fade_distance=20):
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
        # Blit the precomputed gradient surface onto the main surface
        self.screen.blit(self.gradient_surface, (self.ellipse_rect.x, self.ellipse_rect.y))

