"""
This module provides a Star object. Stars perform a function of the moving background.
"""

import random

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Star(Sprite):
    """Star object representing a individual star in the space."""

    __STARS_NAMES: tuple[str, ...] = ("star1.png", "star2.png", "star3.png", "star4.png",
                                      "star5.png", "star6.png", "star7.png", "star8.png",
                                      "star9.png", "star10.png", "star11.png", "star12.png",
                                      "star13.png", "star14.png", "star15.png", "star16.png",
                                      "star17.png", "star18.png")

    def __init__(self, ai_game) -> None:
        """Initialize a random star in a random position (but confined in the y direction)."""
        super().__init__()
        self.settings = ai_game.settings

        # Load the random star.
        star_path: str = f"../assets/stars/{random.choice(self.__STARS_NAMES)}"
        self.image: Surface = pg.image.load(star_path).convert_alpha()
        self.rect: Rect = self.image.get_rect()

        # Initially the star is placed randomly but in the first row of the screen.
        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(0, self.settings.screen_height // self.settings.stars_rows)

        self.y: float = float(self.rect.y)

    def update(self, *args, **kwargs) -> None:
        """Updates the star y-position by its speed defined in settings."""
        self.y += self.settings.star_speed
        self.rect.y = int(self.y)
