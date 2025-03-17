import math
import pygame

import pygame
import math

class Star:
  """
  Represents a 5-pointed star shape in pygame.

  Attributes:
    screen: The pygame display surface to draw on.
    color: The fill color of the star (tuple of RGB values).
    size: A tuple containing the width and height of the star.
    position: A tuple containing the x and y coordinates of the star's center.
    outline_color: The outline color of the star (tuple of RGB values), or None for no outline.
    outline_thickness: The thickness of the outline, defaults to 1.
    inner_star_thickness: The thickness of the inner star, defaults to 0.
  """

  def __init__(self, screen, color, size, position, outline_color=None, outline_thickness=1, inner_star_thickness=0):
    """
    Initializes a new Star object.

    Args:
      screen: The pygame display surface to draw on.
      color: The fill color of the star (tuple of RGB values).
      size: A tuple containing the width and height of the star.
      position: A tuple containing the x and y coordinates of the star's center.
      outline_color: The outline color of the star (tuple of RGB values), or None for no outline (default).
      outline_thickness: The thickness of the outline (default 1).
      inner_star_thickness: The thickness of the inner star (default 0).
    """
    self.screen = screen
    self.color = color
    self.size = size
    self.position = position
    self.outline_color = outline_color
    self.outline_thickness = outline_thickness
    self.inner_star_thickness = inner_star_thickness

  def draw(self):
    """
    Draws the star onto the screen.
    """
    x, y = self.position
    outer_radius = self.size[0] / 2
    inner_radius = outer_radius / 2  # Adjust as needed for star shape

    points = []
    for i in range(10):
      angle = math.pi / 5 * i
      radius = outer_radius if i % 2 == 0 else inner_radius
      point_x = x + radius * math.sin(angle)
      point_y = y - radius * math.cos(angle) # y is inverted in pygame
      points.append((point_x, point_y))

    if self.outline_color:
      outline_points = []
      outline_radius = outer_radius + self.outline_thickness # Increase radius for outline
      outline_inner_radius = inner_radius + self.outline_thickness
      for i in range(10):
        angle = math.pi / 5 * i
        radius = outline_radius if i % 2 == 0 else outline_inner_radius
        point_x = x + radius * math.sin(angle)
        point_y = y - radius * math.cos(angle)
        outline_points.append((point_x, point_y))
      pygame.draw.polygon(self.screen, self.outline_color, outline_points)
    pygame.draw.polygon(self.screen, self.color, points, self.inner_star_thickness)