import pygame
import sys
from pygame.locals import *

class SplashScreen():
    def __init__(self, screen, duration=5000):  # Total duration including fades
        self.screen = screen
        self.duration = duration
        self.fade_duration = 1000  # Duration for each fade in and fade out
        self.start_time = pygame.time.get_ticks()
        
        self.image_path = 'resources/images/splash_image.png'  # Update this path
        self.background_image = pygame.transform.scale(
            pygame.image.load(self.image_path).convert_alpha(),
            self.screen.get_size()
        )
        self.fade_surface = pygame.Surface(self.screen.get_size())
        self.fade_surface.fill((0,0,0))
        self.state = 'fade_in'

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

    def fade_in(self, elapsed_time):
        alpha = 255 * (elapsed_time / self.fade_duration)
        self.fade_surface.set_alpha(255 - min(alpha, 255))
        self.screen.blit(self.fade_surface, (0, 0))
        if elapsed_time >= self.fade_duration:
            self.state = 'display'

    def fade_out(self, elapsed_time):
        alpha = 255 * ((elapsed_time - self.duration + self.fade_duration) / self.fade_duration)
        self.fade_surface.set_alpha(min(alpha, 255))
        self.screen.blit(self.fade_surface, (0, 0))
        if elapsed_time >= self.duration:
            self.state = 'done'

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks() - self.start_time
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                    
            self.draw()
            if self.state == 'fade_in':
                self.fade_in(current_time)
            elif self.state == 'display':
                if current_time >= self.duration - self.fade_duration:
                    self.state = 'fade_out'
            elif self.state == 'fade_out':
                self.fade_out(current_time)
            elif self.state == 'done':
                running = False

            pygame.display.update()