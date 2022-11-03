"""
General module with the player's spaceship implementation.
"""

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Spaceship(Sprite):
    """ Class representing player's spaceship. """

    __RESIZED_SHIP: str = "../assets/player_ships/SF02_resized.png"
    __NORMAL_SHIP: str = "../assets/player_ships/SF02.png"

    def __init__(self, ai_game, resized: bool = False) -> None:
        """ Initialization of spaceship and its initial position. """
        super().__init__()
        self.screen: Surface = ai_game.screen
        self.screen_rect: Rect = ai_game.screen_rect
        self.settings = ai_game.settings

        ship_path: str = self.__NORMAL_SHIP
        if resized:
            ship_path = self.__RESIZED_SHIP

        self.image: Surface = pg.image.load(ship_path).convert_alpha()
        self.rect: Rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 20

        # Position is represented as a float - more accurate position tracking.
        self.x: float = float(self.rect.x)
        self.moving_right: bool = False
        self.moving_left: bool = False

    def update(self, *args, **kwargs) -> None:
        """ Update the spaceship x-position by its speed defined in settings. """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.player_ship_speed

        # Usage of elif - priority for moving right.
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.player_ship_speed

        self.rect.x = int(self.x)

    def centre_spaceship(self) -> None:
        """ Place the spaceship in the centre of the screen. """
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 20
        self.x = float(self.rect.x)

    def draw_spaceship(self) -> None:
        """ Displays the spaceship in current position on the screen. """
        self.screen.blit(self.image, self.rect)
