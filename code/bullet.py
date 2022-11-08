"""
This module provides a Bullet object, which can be fired by Alien or Player.
"""

import random

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.mixer import Sound


class Bullet(Sprite):
    """Bullet object provides a bullet, which can be fired by Alien or Player."""

    __ALIEN_BULLET_PATH: str = "../assets/bullets/alien_bullet.png"
    __GENERAL_BULLET_PATH: str = "../assets/bullets/general_bullet.png"
    __PLAYER_BULLET_PATH: str = "../assets/bullets/player_bullet.png"
    __FIRE_SOUND_PATH: str = "../sounds/fire.wav"

    image: Surface
    rect: Rect
    y: float
    direction: int
    speed: float
    fire_sound: Sound | None

    def __init__(self, ai_game, owner: str) -> None:
        """
        Create bullet in the current player's or alien's position.

        Parameters:
        -----------
        owner : `str`
            Bullet owner, it can be "Player" or "Alien".
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        if owner == "Player":
            self._initialize_player_bullet(ai_game)
        elif owner == "Alien":
            self._initialize_alien_bullet(ai_game)

    def _initialize_player_bullet(self, ai_game) -> None:
        """Initialize atributes related to player's bullet."""
        self.image = pg.image.load(self.__PLAYER_BULLET_PATH).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.player_ship.rect.midtop
        self.y = float(self.rect.y)
        # Bullet moves to the top of the screen
        self.direction = -1
        self.speed = self.settings.player_bullet_speed
        # Fire sound is only related to player's bullet.
        self.fire_sound = pg.mixer.Sound(self.__FIRE_SOUND_PATH)

    def _initialize_alien_bullet(self, ai_game) -> None:
        """Initialize atributes related to alien's bullet."""
        # Alien's general will always appear on the final level.
        if ai_game.aliens_ships:
            chosen_alien = random.choice(list(ai_game.aliens_ships))
            self.image = pg.image.load(self.__ALIEN_BULLET_PATH).convert_alpha()
        else:
            chosen_alien = ai_game.aliens_general
            self.image = pg.image.load(self.__GENERAL_BULLET_PATH).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = chosen_alien.rect.midbottom
        self.y = float(self.rect.y)
        # Bullet moves to the bottom of the screen
        self.direction = 1
        self.speed = self.settings.alien_bullet_speed
        # The sound is related only to the player.
        self.fire_sound = None

    def play_sound(self) -> None:
        """Plays the sound if the player fires a bullet."""
        if self.fire_sound:
            self.fire_sound.play()

    def update(self, *args, **kwargs) -> None:
        """Updates the bullet's position on the screen."""
        self.y += self.direction*self.speed
        self.rect.y = int(self.y)

    def draw(self) -> None:
        """Displays a bullet on the screen."""
        self.screen.blit(self.image, self.rect)
