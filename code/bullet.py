'''
General file representing bullet.
'''

import random

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Bullet(Sprite):
    ''' Represents bullet fired by a spaceship. '''

    __PLAYER_BULLET_IMG: str = '../images/player_bullet.png'
    __ALIEN_BULLET_PATH: str = '../images/alien_bullet.png'
    __FIRE_SOUND_PATH: str = '../sounds/fire.wav'
    direction: int
    bullet_speed: float

    def __init__(self, ai_game, owner: str) -> None:
        ''' Create bullet in current spaceship position. '''
        super().__init__()
        self.screen: Surface = ai_game.screen
        self.settings = ai_game.settings

        if owner == 'player':
            # Create bullet rect and its position
            self.image: Surface = pg.image.load(self.__PLAYER_BULLET_IMG).convert_alpha()
            self.rect: Rect = self.image.get_rect()
            self.rect.midtop = ai_game.ship.rect.midtop
            self.direction = -1
            self.bullet_speed = self.settings.player_bullet_speed
            self.fire_sound = pg.mixer.Sound(self.__FIRE_SOUND_PATH)
        elif owner == 'alien':
            self.image = pg.image.load(self.__ALIEN_BULLET_PATH).convert_alpha()
            self.rect = self.image.get_rect()
            random_alien = random.choice(list(ai_game.aliens_ships))
            self.rect.midbottom = random_alien.rect.midbottom
            self.direction = 1
            self.bullet_speed = self.settings.alien_bullet_speed

        self.y: float = float(self.rect.y)

    def update(self, *args, **kwargs) -> None:
        ''' Bullet movement of the screen. '''
        self.y += self.direction*self.bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self) -> None:
        ''' Displays bullet on the screen. '''
        self.screen.blit(self.image, self.rect)
