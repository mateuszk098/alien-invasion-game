'''
General file with alien class.
'''

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    ''' Class representing a individual alien ship. '''

    def __init__(self, ai_game) -> None:
        ''' Initialize the alien ship. '''
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien ship image and load its rect.
        self.image = pygame.image.load('images/alienship_resized.png')
        self.rect = self.image.get_rect()

        # Place alien ship near the top-left screen edge.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x: float = float(self.rect.x)
