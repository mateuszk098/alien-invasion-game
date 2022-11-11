"""
This module provides AlienSoldier and AlienGeneral objects. AlienSoldier objects 
are usual enemies in the game. AlienGeneral is the final enemy. Both objects 
inherit from the Alien class, which is the abstract base class. The Alien inherits 
from Sprite.
"""

from abc import ABCMeta, abstractmethod

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Alien(Sprite, metaclass=ABCMeta):
    """The Alien class provide an abstract base class for AlienSoldier and AlienGeneral."""

    @abstractmethod
    def __init__(self, ai_game, img, speed) -> None:
        """Initialise the Alien base."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect: Rect = ai_game.screen_rect
        self.image: Surface = pg.image.load(img).convert_alpha()
        self.rect: Rect = self.image.get_rect()
        # The alien's speed is constant on each next gameplay level, so one can pass it in the `__init__()` method.
        self.speed: float = speed
        # Float type for the horizontal position due to more accurate tracking.
        self.x: float

    def check_left_right_screen_edge(self) -> bool:
        """
        Returns true if the alien ship is near the left or right
        edge of the screen; otherwise, it returns false.
        """
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
        return False


class AlienSoldier(Alien):
    """AlienSoldier provides an ordinary alien ship object, which depends on the game's difficulty mode."""

    _IMGS: tuple[str, ...] = ("perseus_arm_alien.png", "outer_arm_alien.png", "norma_arm_alien.png")

    def __init__(self, ai_game) -> None:
        """Initialise AlienSoldier object."""
        self.settings = ai_game.settings
        ship_model: int = self.settings.alien_ship_model
        img: str = f"../assets/aliens_ships/{self._IMGS[ship_model-1]}"
        speed: float = self.settings.alien_ship_speed
        super().__init__(ai_game, img, speed)
        self.x: float = float(self.rect.x)

    def update(self, *args, **kwargs) -> None:  # Override the Sprite.update()
        """Updates the alien ship's x-position by speed defined in settings."""
        self.x += self.settings.alien_moving_direction*self.speed
        self.rect.x = int(self.x)


class AlienGeneral(Alien):
    """
    AlienGeneral provides a final alien ship object, which depends on the game's difficulty mode. 
    This alien ship has a dedicated life bar.
    """

    _IMGS: tuple[str, ...] = ("perseus_arm_general.png", "outer_arm_general.png", "norma_arm_general.png")

    def __init__(self, ai_game) -> None:
        """Initialise AlienGeneral object."""
        self.settings = ai_game.settings
        ship_model: int = self.settings.alien_general_ship_model
        img: str = f"../assets/aliens_ships/{self._IMGS[ship_model-1]}"
        speed: float = self.settings.alien_general_ship_speed
        super().__init__(ai_game, img, speed)

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.settings.screen_height // 3
        self.x: float = float(self.rect.x)

        self.life_points: int = self.settings.alien_general_life_points
        self.life_bar_color = self.settings.alien_general_life_bar_color
        self.life_bar_outline_color = self.settings.alien_general_life_bar_outline_color
        self.life_bar_rect: Rect = pg.Rect(0, 0, self.life_points, 15)

        # Place the life bar above the generalship.
        self.life_bar_rect.centerx = self.rect.centerx
        self.life_bar_rect.y = self.rect.top - 20

    def reset_alien_general_ship(self) -> None:
        """Resets aliens' generalship position and its life bar length to the initial state."""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.settings.screen_height // 3
        self.x = float(self.rect.x)

        self.life_points = self.settings.alien_general_life_points
        self.life_bar_rect.centerx = self.rect.centerx
        self.life_bar_rect.y = self.rect.top - 20

    def update(self, *args, **kwargs) -> None:  # Override the Sprite.update()
        """Updates aliens' generalship position and its life bar length."""
        self.x += self.settings.alien_moving_direction*self.settings.alien_general_ship_speed
        self.rect.x = int(self.x)

        self.life_bar_rect = pg.Rect(0, 0, self.life_points, 15)
        self.life_bar_rect.centerx = self.rect.centerx
        self.life_bar_rect.y = self.rect.top - 20

    def draw(self) -> None:
        """Displays aliens' generalship and its life bar on the screen."""
        self.screen.blit(self.image, self.rect)
        pg.draw.rect(self.screen, self.life_bar_color, self.life_bar_rect)
        pg.draw.rect(self.screen, self.life_bar_outline_color, self.life_bar_rect, 2)  # 2 means width of the outline.
