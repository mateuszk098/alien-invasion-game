"""
General file representing bullet.
"""

import random

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class PlayerBullet(Sprite):
    """ Represents bullet fired by a player's spaceship. """

    __PLAYER_BULLET_IMG: str = "../assets/bullets/player_bullet.png"
    __FIRE_SOUND_PATH: str = "../sounds/fire.wav"

    def __init__(self, ai_game) -> None:
        """ Create a bullet in the current spaceship position. """
        super().__init__()
        self.screen: Surface = ai_game.screen
        self.settings = ai_game.settings

        self.fire_sound = pg.mixer.Sound(self.__FIRE_SOUND_PATH)

        # Create bullet rect and its position
        self.image: Surface = pg.image.load(self.__PLAYER_BULLET_IMG).convert_alpha()
        self.rect: Rect = self.image.get_rect()

        self.rect.midtop = ai_game.player_ship.rect.midtop
        self.y: float = float(self.rect.y)

    def update(self, *args, **kwargs) -> None:
        """ Bullet movement of the screen. """
        self.y -= self.settings.player_bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self) -> None:
        """ Displays bullet on the screen. """
        self.screen.blit(self.image, self.rect)


class AlienBullet(Sprite):
    """ Represents bullet fired by alien's ship. """

    __ALIEN_BULLET_PATH: str = "../assets/bullets/alien_bullet.png"

    def __init__(self, ai_game) -> None:
        """ Create a bullet in the position of a randomly selected alien's ship. """
        super().__init__()
        self.screen: Surface = ai_game.screen
        self.settings = ai_game.settings

        self.image: Surface = pg.image.load(self.__ALIEN_BULLET_PATH).convert_alpha()
        self.rect: Rect = self.image.get_rect()

        if ai_game.aliens_ships:
            chosen_alien = random.choice(list(ai_game.aliens_ships))
        else:
            chosen_alien = ai_game.aliens_general
        self.rect.midbottom = chosen_alien.rect.midbottom
        self.y: float = float(self.rect.y)

    def update(self, *args, **kwargs) -> None:
        """ Bullet movement of the screen. """
        self.y += self.settings.alien_bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self) -> None:
        """ Displays bullet on the screen. """
        self.screen.blit(self.image, self.rect)
