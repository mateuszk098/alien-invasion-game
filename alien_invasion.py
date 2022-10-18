'''
General file with class used to game management.
'''

import sys

import pygame

from settings import Settings
from spaceship import Spaceship
from bullet import Bullet
from alien import Alien
from star import Star


class AlienInvasion():
    ''' General class to game management. '''

    def __init__(self) -> None:
        ''' Game initialization. '''
        pygame.init()  # Initialization of screen.
        pygame.display.set_caption('Alien Invasion')

        self.settings: Settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # Full screen.
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.ship: Spaceship = Spaceship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_stars()

    def run_game(self) -> None:
        ''' Main loop of the game. '''
        while True:
            self._check_events()
            self._update_stars()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_events(self) -> None:
        ''' Check reaction to button press and mouse interaction. '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event) -> None:
        ''' Reaction on key press. '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event) -> None:
        ''' Reaction on key release. '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self) -> None:
        ''' Create new bullet and add it to group. '''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet: Bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self) -> None:
        ''' Update of bullets positions and remove bullets from out of screen. '''
        self.bullets.update()
        # Remove bullets out of the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:  # type: ignore
                self.bullets.remove(bullet)

    def _create_fleet(self) -> None:
        ''' Create new alien fleet. '''
        alien: Alien = Alien(self)

        alien_width: int = alien.rect.width  # type: ignore
        available_space_x: int = self.settings.screen_width - (2*alien_width)
        number_aliens_x: int = available_space_x // (2*alien_width)

        alien_height: int = alien.rect.height  # type: ignore
        ship_height: int = self.ship.rect.height
        available_space_y: int = self.settings.screen_height - (3*alien_height) - ship_height
        number_rows: int = available_space_y // (2*alien_height)

        # Create the fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number: int, row_number: int) -> None:
        ''' Create new alien and add it to the row. '''
        alien: Alien = Alien(self)
        alien_width: int = alien.rect.width  # type: ignore
        alien_height: int = alien.rect.height  # type: ignore
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x  # type: ignore
        alien.rect.y = alien.rect.height + 2*alien_height*row_number  # type: ignore
        self.aliens.add(alien)

    def _update_aliens(self) -> None:
        ''' Update all aliens position on the screen. '''
        self.aliens.update()

    def _create_stars(self) -> None:
        ''' Create outer space with stars. '''
        pixels_per_row: int = self.settings.screen_height // self.settings.star_rows

        for row in range(self.settings.star_rows):
            for _ in range(self.settings.stars_per_row):
                star: Star = Star(self)
                star.y += pixels_per_row*row
                star.rect.y = star.y  # type: ignore
                self.stars.add(star)

    def _update_stars(self) -> None:
        ''' Update all stars position on the screen. '''
        self.stars.update()

        for star in self.stars.copy():
            if star.rect.top > self.settings.screen_height:  # type: ignore
                self.stars.remove(star)

        pixels_per_row: int = self.settings.screen_height // self.settings.star_rows

        if len(self.stars) < self.settings.stars_per_row*self.settings.star_rows:
            new_star: Star = Star(self)
            # Provide effect that stars coming on the screen naturally.
            new_star.y -= pixels_per_row
            new_star.rect.y = new_star.y  # type: ignore
            self.stars.add(new_star)

    def _update_screen(self) -> None:
        ''' Updates the screen. '''
        self.screen.fill(self.settings.background_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # type: ignore
        self.aliens.draw(self.screen)
        pygame.display.flip()  # Update of the screen.


if __name__ == '__main__':
    # Instance of game
    ai: AlienInvasion = AlienInvasion()
    ai.run_game()
