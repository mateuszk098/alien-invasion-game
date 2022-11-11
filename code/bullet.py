"""
This module provides PlayerBullet, AlienSoldierBullet and AlienGeneralBullet objects. 
These objects are the most common in the game. Each of them inherits from Bullet, 
the abstract base class. The Bullet inherits from Sprite.
"""

from random import choice
from abc import ABCMeta, abstractmethod

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Bullet(Sprite, metaclass=ABCMeta):
    """The Bullet class provide an abstract base class for the other objects."""

    @abstractmethod
    def __init__(self, ai_game, img, direction, speed) -> None:
        """Initialise Bullet base object."""
        super().__init__()
        self.image: Surface = pg.image.load(img).convert_alpha()
        self.rect: Rect = self.image.get_rect()
        self.direction: int = direction
        # The bullet's speed is constant on each next gameplay level, so one can pass it in the `__init__()` method.
        self.speed: float = speed
        # Float type for the vertical position due to more accurate tracking.
        self.y: float

    def update(self, *args, **kwargs) -> None:  # Override the Sprite.update()
        """Updates the bullet's y-position by the speed defined in settings."""
        self.y += self.direction*self.speed
        self.rect.y = int(self.y)


class PlayerBullet(Bullet):
    """PlayerBullet provides a bullet which the player can fire."""

    _IMG: str = "../assets/bullets/player_bullet.png"
    _DIRECTION: int = -1  # The bullet moves to the top of the screen.
    _SOUND: str = "../sounds/fire.wav"

    def __init__(self, ai_game) -> None:
        """Initialise PlayerBullet object."""
        super().__init__(ai_game, self._IMG, self._DIRECTION, ai_game.settings.player_bullet_speed)
        self.rect.midtop = ai_game.player_ship.rect.midtop
        self.y = float(self.rect.y)
        self.fire_sound = pg.mixer.Sound(self._SOUND)

    def play_sound(self) -> None:
        """Plays the sound if the player fires a bullet."""
        self.fire_sound.play()


class AlienSoldierBullet(Bullet):
    """AlienSoldierBullet provides a bullet which the alien can fire."""

    _IMG: str = "../assets/bullets/alien_bullet.png"
    _DIRECTION: int = 1  # The bullet moves to the bottom of the screen.

    def __init__(self, ai_game) -> None:
        """Initialise AlienSoldierBullet object."""
        super().__init__(ai_game, self._IMG, self._DIRECTION, ai_game.settings.alien_bullet_speed)
        # The bullet initial position is associated with a random alien ship.
        random_alien = choice(list(ai_game.alien_soldier_ships))
        self.rect.center = random_alien.rect.midbottom
        self.y = float(self.rect.y)


class AlienGeneralBullet(Bullet):
    """AlienGeneralBullet provides a bullet which the alien's general can fire."""

    _IMG: str = "../assets/bullets/general_bullet.png"
    _DIRECTION: int = 1

    def __init__(self, ai_game) -> None:
        """Initialise AlienGeneralBullet object."""
        super().__init__(ai_game, self._IMG, self._DIRECTION, ai_game.settings.alien_bullet_speed)
        self.rect.center = ai_game.alien_general_ship.rect.midbottom
        self.y = float(self.rect.y)
