'''
General file representing bullet.
'''

import random

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Bullet(Sprite):
    ''' Represents bullet fired by a spaceship. '''

    __BULLET_IMG: str = '../images/bullet.png'

    def __init__(self, ai_game, owner: str) -> None:
        ''' Create bullet in current spaceship position. '''
        super().__init__()
        self.screen: Surface = ai_game.screen
        self.settings = ai_game.settings

        # Create bullet rect and its position
        self.image: Surface = pygame.image.load(self.__BULLET_IMG).convert_alpha()
        self.rect: Rect = self.image.get_rect()

        if owner == 'player':
            self.rect.midtop = ai_game.ship.rect.midtop
            self.direction: int = -1
        elif owner == 'alien':
            random_alien = random.choice(list(ai_game.aliens_ships))
            self.rect.midbottom = random_alien.rect.midbottom
            self.direction = 1

        self.y: float = float(self.rect.y)

    def update(self, *args, **kwargs) -> None:
        ''' Bullet movement of the screen. '''
        self.y += self.direction*self.settings.bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self) -> None:
        ''' Displays bullet on the screen. '''
        self.screen.blit(self.image, self.rect)
