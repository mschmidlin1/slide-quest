








import pygame
from sq_src.sprites.notification_banner import NotificationBanner
from sq_src.metas import SingletonMeta


class BannerManager(metaclass=SingletonMeta):
    """
    Manages the display and lifecycle of notification banners on the screen.

    This class uses the Singleton pattern to ensure that only one instance of the
    banner manager exists throughout the application. It handles the creation,
    updating, and drawing of notification banners using a Pygame sprite group.

    Attributes:
        screen (pygame.surface.Surface): The Pygame surface on which to draw the banners.
        banner_sprite_group (pygame.sprite.LayeredUpdates): A sprite group to manage the banners.
    """

    def __init__(self, screen: pygame.surface.Surface):
        """
        Initializes the BannerManager.

        Args:
            screen (pygame.surface.Surface): The Pygame surface to draw banners on.
        """
        self.screen = screen
        self.banner_sprite_group = pygame.sprite.LayeredUpdates()

    def add_banner(self, text: str, duration_s: float, **kwargs):
        """
        Adds a new notification banner to the screen.

        Args:
            text (str): The text to display on the banner.
            duration_s (float): The duration of the banner in seconds.
            **kwargs: Additional keyword arguments to pass to the NotificationBanner constructor.
        """
        self.banner_sprite_group.add(NotificationBanner(text, duration_s, **kwargs))

    def update(self, events: list[pygame.event.Event]):
        """
        Updates all active notification banners.

        Args:
            events (list[pygame.event.Event]): A list of Pygame events (not used in this method).
        """
        self.banner_sprite_group.update()

    def draw(self):
        """
        Draws all active notification banners on the screen.
        """
        self.banner_sprite_group.draw(self.screen)