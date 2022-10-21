'''
General file with class to user spaceship management.
'''

import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite


class Spaceship(Sprite):
    ''' Class to user spaceship management. '''

    __RESIZED_SHIP: str = '../images/spaceship_resized.png'
    __NORMAL_SHIP: str = '../images/spaceship.png'

    def __init__(self, ai_game, resized=False) -> None:
        ''' Initialization of spaceship and its initial position. '''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the spaceship image and load its rect.
        if resized is True:
            self.image = pygame.image.load(self.__RESIZED_SHIP)
        else:
            self.image = pygame.image.load(self.__NORMAL_SHIP)
        self.rect: Rect = self.image.get_rect()

        # Every new spaceship occurs at te bottom of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Position and moving.
        self.x: float = float(self.rect.x)  # Position is represented as a float
        self.moving_right: bool = False
        self.moving_left: bool = False

    def update(self, *args, **kwargs) -> None:
        ''' Update of the spaceship position considering flag indicating its moving. '''
        if self.moving_right is True and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        # Usage of elif - priority for moving right.
        if self.moving_left is True and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = int(self.x)

    def center_ship(self) -> None:
        ''' Place the ship in the center of the screen. '''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self) -> None:
        ''' Displays the spaceship in current position on the screen. '''
        self.screen.blit(self.image, self.rect)
