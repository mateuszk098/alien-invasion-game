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

    def blitme(self) -> None:
        ''' Displays the spaceship in current position on the screen. '''
        self.screen.blit(self.image, self.rect)
