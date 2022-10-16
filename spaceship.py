'''
General file with class to user spaceship management.
'''

import pygame


class Spaceship():
    ''' Class to user spaceship management. '''

    def __init__(self, ai_game) -> None:
        ''' Initialization of spaceship and its initial position. '''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the spaceship image and load its rect.
        self.image = pygame.image.load('images/spaceship1_resized.png')
        self.rect = self.image.get_rect()

        # Every new spaceship occurs at te bottom of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right: bool = False
        self.moving_left: bool = False

    def update(self) -> None:
        ''' Update of the spaceship position considering flag indicating its moving. '''
        if self.moving_right == True:
            self.rect.x += 1
        if self.moving_left == True:  # Usage of elif - priority for moving right.
            self.rect.x -= 1

    def blitme(self) -> None:
        ''' Displays the spaceship in current position on the screen. '''
        self.screen.blit(self.image, self.rect)
