'''
General file with star class.
'''

import random

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Star(Sprite):
    ''' Class representing a individual star in the space. '''

    __MY_STARS: tuple[str, ...] = ('star1.png', 'star2.png', 'star3.png', 'star4.png',
                                   'star5.png', 'star6.png', 'star7.png', 'star8.png',
                                   'star9.png', 'star10.png', 'star11.png', 'star12.png',
                                   'star13.png', 'star14.png', 'star15.png')

    def __init__(self, ai_game) -> None:
        ''' Initialize a random star in random position (but confined in y direction). '''
        super().__init__()
        self.settings = ai_game.settings

        # Load the random star image and load its rect.
        star_path: str = f'../images/{random.choice(self.__MY_STARS)}'
        self.image: Surface = pygame.image.load(star_path).convert_alpha()
        self.rect: Rect = self.image.get_rect()

        # Place star at the top row.
        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(0, self.settings.screen_height // self.settings.star_rows)

        self.y: float = float(self.rect.y)

    def update(self, *args, **kwargs) -> None:
        ''' Update stars position. '''
        self.y += self.settings.stars_speed
        self.rect.y = int(self.y)
