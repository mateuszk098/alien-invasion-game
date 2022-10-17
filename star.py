'''
General file with star class.
'''

import random

import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    ''' Class representing a individual star in the space. '''

    __my_stars: list[str] = ['star1.png', 'star2.png', 'star3.png', 'star4.png',
                             'star5.png', 'star6.png', 'star7.png', 'star8.png',
                             'star9.png', 'star10.png', 'star11.png', 'star12.png',
                             'star13.png', 'star14.png', 'star15.png']

    def __init__(self, ai_game) -> None:
        ''' Initialize a star. '''
        super().__init__()

        # Load the random star image and load its rect.
        self.image = pygame.image.load(f'images/{random.choice(self.__my_stars)}')
        self.rect = self.image.get_rect()

        # Place star at the left corner.
        self.rect.x = random.randint(0, ai_game.settings.screen_width)
        self.rect.y = random.randint(0, ai_game.settings.screen_height // ai_game.settings.star_rows)

        self.y: float = float(self.rect.y)
