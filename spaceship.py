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
        self.settings = ai_game.settings

        # Load the spaceship image and load its rect.
        self.image = pygame.image.load('images/spaceship1_resized.png')
        self.rect = self.image.get_rect()

        # Every new spaceship occurs at te bottom of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Position and moving.
        self.x: float = float(self.rect.x)  # Position is represented as a float
        self.moving_right: bool = False
        self.moving_left: bool = False

    def update(self) -> None:
        ''' Update of the spaceship position considering flag indicating its moving. '''
        if self.moving_right == True and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        # Usage of elif - priority for moving right.
        if self.moving_left == True and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = int(self.x)

    def blitme(self) -> None:
        ''' Displays the spaceship in current position on the screen. '''
        self.screen.blit(self.image, self.rect)
