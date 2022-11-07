"""
This module provides a button object, used by the menu object.
"""

import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect


class Button():
    """Button object provides communication with the player using a mouse."""

    def __init__(self, ai_game, text: str, **kwargs) -> None:
        """
        Initialize default button properties like as size and text.

        Parameters:
        -----------
        **kwargs : `dict`, `optional`
            width : `int`, default=250
            height : `int`, default=50
            fontsize : `int`, default=48
            offset : `int`, default=0
                Initial position on the screen. Default value is 0, which means the centre
                of the screen. It can be positive or negative.
        """
        self.screen: Surface = ai_game.screen
        self.screen_rect: Rect = ai_game.screen_rect

        self.width: int = kwargs.get("width", 250)
        self.height: int = kwargs.get("height", 50)

        self.text_color = pg.Color("#f0f0f0")
        self.released_color = pg.Color("#154360")
        self.pressed_color = pg.Color("#60ce80")

        fontsize: int = kwargs.get("fontsize", 48)
        self.font = pg.font.SysFont("freesansbold", fontsize)

        self.rect: Rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        offset: int = kwargs.get("offset", 0)
        self.rect.y += offset

        self.text_img: Surface = self.font.render(text, True, self.text_color)
        self.text_rect: Rect = self.text_img.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, is_pressed: bool = False) -> None:
        """Draws a button rect with the message on the screen."""
        current_color = self.released_color
        if is_pressed:
            current_color = self.pressed_color

        self.screen.fill(current_color, self.rect)
        self.screen.blit(self.text_img, self.text_rect)
