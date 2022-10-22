'''
General file representing bullet.
'''

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Bullet(Sprite):
    ''' Represents bullet fired by a spaceship. '''

    __BULLET_IMG: str = '../images/bullet.png'

    def __init__(self, ai_game) -> None:
        ''' Create bullet in current spaceship position. '''
        super().__init__()
        self.screen: Surface = ai_game.screen
        self.settings = ai_game.settings
        self.color: int = self.settings.bullet_color

        # Create bullet rect and its position
        self.image: Surface = pygame.image.load(self.__BULLET_IMG)
        self.rect: Rect = self.image.get_rect()
        # self.rect: Rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y: float = float(self.rect.y)

    def update(self, *args, **kwargs) -> None:
        ''' Bullet movement of the screen. '''
        self.y -= self.settings.bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self) -> None:
        ''' Displays bullet on the screen. '''
        #pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
