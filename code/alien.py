'''
General module with an alien implementation.
'''

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Alien(Sprite):
    ''' Class representing an individual alien ship. '''

    __ALIEN_PATH: str = '../images/alienship.png'

    def __init__(self, ai_game) -> None:
        ''' Initialise the alien ship. '''
        super().__init__()
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings

        self.image: Surface = pg.image.load(self.__ALIEN_PATH).convert_alpha()
        self.rect: Rect = self.image.get_rect()

        # Place the alien ship near the top-left screen edge.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x: float = float(self.rect.x)

    def check_left_right_screen_edge(self) -> bool:
        ''' 
        Returns true if the alien ship is near the left or right 
        edge of the screen; otherwise, it returns false. 
        '''
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self, *args, **kwargs) -> None:
        ''' Updates alien ship x-position by speed displacement defined in settings. '''
        self.x += self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x = int(self.x)
