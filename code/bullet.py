"""
This module provides a Bullet objects, which can be fired by Alien or Player.
"""

from random import choice
from abc import ABCMeta, abstractmethod

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Bullet(Sprite, metaclass=ABCMeta):
    """Bullet object provides a base abstract bullet object."""

    @abstractmethod
    def __init__(self, ai_game, img, direction, speed) -> None:
        super().__init__()
        self.image: Surface = pg.image.load(img).convert_alpha()
        self.rect: Rect = self.image.get_rect()
        self.direction: int = direction
        self.speed: float = speed
        self.y: float  # Float type for vertical position due to more accurate tracking.

    def update(self, *args, **kwargs) -> None:
        """Updates the bullet's position on the screen."""
        self.y += self.direction*self.speed
        self.rect.y = int(self.y)


class PlayerBullet(Bullet):
    """PlayerBullet provides a bullet, which can be fired by the user."""

    __IMG: str = "../assets/bullets/player_bullet.png"
    __DIRECTION: int = -1
    __SOUND: str = "../sounds/fire.wav"

    def __init__(self, ai_game) -> None:
        super().__init__(ai_game, self.__IMG, self.__DIRECTION, ai_game.settings.player_bullet_speed)
        self.rect.midtop = ai_game.player_ship.rect.midtop
        self.y = float(self.rect.y)
        self.fire_sound = pg.mixer.Sound(self.__SOUND)

    def play_sound(self) -> None:
        """Plays the sound if the player fires a bullet."""
        self.fire_sound.play()


class AlienBullet(Bullet):
    """AlienBullet provides a bullet, which can be fired by the alien."""

    __IMG: str = "../assets/bullets/alien_bullet.png"
    __DIRECTION: int = 1

    def __init__(self, ai_game) -> None:
        super().__init__(ai_game, self.__IMG, self.__DIRECTION, ai_game.settings.alien_bullet_speed)
        # Bullet is associated with a random alien's ship.
        random_alien = choice(list(ai_game.aliens_ships))
        self.rect.center = random_alien.rect.midbottom
        self.y = float(self.rect.y)


class GeneralBullet(Bullet):
    """GeneralBullet provides a bullet, which can be fired by the aliens' general."""

    __IMG: str = "../assets/bullets/general_bullet.png"
    __DIRECTION: int = 1

    def __init__(self, ai_game) -> None:
        super().__init__(ai_game, self.__IMG, self.__DIRECTION, ai_game.settings.alien_bullet_speed)
        self.rect.center = ai_game.aliens_general.rect.midbottom
        self.y = float(self.rect.y)
