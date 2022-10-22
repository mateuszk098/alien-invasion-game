'''
General file with alien class.
'''

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Alien(Sprite):
    ''' Class representing a individual alien ship. '''

    __ALIEN_IMG: str = '../images/alienship.png'

    def __init__(self, ai_game) -> None:
        ''' Initialize the alien ship. '''
        super().__init__()
        self.screen: Surface = ai_game.screen
        self.screen_rect: Rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Load the alien ship image and load its rect.
        self.image: Surface = pygame.image.load(self.__ALIEN_IMG)
        self.rect: Rect = self.image.get_rect()

        # Place alien ship near the top-left screen edge.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x: float = float(self.rect.x)

    def check_edges(self) -> bool:
        ''' Returns true if alien ship is near the edge of the screen. '''
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self, *args, **kwargs) -> None:
        ''' Updates alien ship position by given pixels. '''
        self.x += self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x = int(self.x)
