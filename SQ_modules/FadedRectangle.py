import pygame
from SQ_modules.configs import BLUE_ICE
from SQ_modules.DataTypes import Point, Size






class FadedRectangle:
    def __init__(self, screen: pygame.surface.Surface, center: Point, size: Size, color, fade_distance=20):
        self.screen = screen
        self.center = center
        self.size = size
        self.color = color
        self.fade_distance = fade_distance
        self.left = center.x-(size.width//2)
        self.top = center.y-(size.height//2)
        self.ellipse_rect = pygame.Rect(self.left, self.top, self.size.width, self.size.height)
        
        







    def draw(self):
        #pygame.draw.ellipse(self.screen, self.color, self.ellipse_rect)



        # # Create a temporary surface with per-pixel alpha
        # temp_surface = pygame.Surface((self.ellipse_rect.width, self.ellipse_rect.height), pygame.SRCALPHA)
        # pygame.draw.ellipse(temp_surface, self.color + (255,), [0, 0, self.ellipse_rect.width, self.ellipse_rect.height])

        # # Modify alpha of pixels to create the fade effect
        # for x in range(self.ellipse_rect.width):
        #     for y in range(self.ellipse_rect.height):
        #         if pygame.Color(temp_surface.get_at((x, y)).a) != 0:
        #             # Calculate distance to the nearest edge
        #             distance_x = min(x, self.ellipse_rect.width - x)
        #             distance_y = min(y, self.ellipse_rect.height - y)
        #             distance = min(distance_x, distance_y)
                    
        #             # Adjust alpha based on distance
        #             alpha = max(0, min(255, int(255 * (distance / self.fade_distance))))
        #             if distance <= self.fade_distance:
        #                 current_color = temp_surface.get_at((x, y))
        #                 temp_surface.set_at((x, y), current_color[:-1] + (alpha,))

        # # Blit the temporary surface onto the main surface
        # self.screen.blit(temp_surface, (self.ellipse_rect.x, self.ellipse_rect.y))


        temp_surface = pygame.Surface((self.ellipse_rect.width, self.ellipse_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, self.color + (255,), [0, 0, self.ellipse_rect.width, self.ellipse_rect.height])

        # Modify alpha of pixels to create the fade effect
        for x in range(self.ellipse_rect.width):
            for y in range(self.ellipse_rect.height):
                # Calculate distance to the nearest edge
                distance_x = min(x, self.ellipse_rect.width - x - 1)
                distance_y = min(y, self.ellipse_rect.height - y - 1)
                distance = min(distance_x, distance_y)
                
                # Adjust alpha based on distance
                alpha = max(0, min(255, int(255 * (distance / self.fade_distance))))
                if distance <= self.fade_distance:
                    current_color = temp_surface.get_at((x, y))
                    temp_surface.set_at((x, y), current_color[:-1] + (alpha,))

        # Blit the temporary surface onto the main surface
        self.screen.blit(temp_surface, (self.ellipse_rect.x, self.ellipse_rect.y))