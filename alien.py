'''
General file with alien class.
'''

import pygame
from pygame.sprite import Sprite
from pygame.rect import Rect


class Alien(Sprite):
    ''' Class representing a individual alien ship. '''

    def __init__(self, ai_game) -> None:
        ''' Initialize the alien ship. '''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien ship image and load its rect.
        self.image = pygame.image.load('images/alienship_other_resized.png')
        self.rect: Rect = self.image.get_rect()

        # Place alien ship near the top-left screen edge.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x: float = float(self.rect.x)

    def update(self, *args, **kwargs) -> None:
        ''' Move alien ship to right. '''
        self.x += self.settings.alien_speed
        self.rect.x = int(self.x)
