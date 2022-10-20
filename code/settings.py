'''
General file to game settings management.
'''

from ctypes.wintypes import RGB


class Settings():
    ''' Holds all settings of game. '''

    def __init__(self) -> None:
        ''' Initialize settings of game. '''
        # Settings related to game screen.
        self.screen_width: int = 1280
        self.screen_height: int = 720
        self.background_color: int = RGB(5, 5, 10)

        # Settings related to spaceship.
        self.ship_speed: float
        self.ship_limit: int = 3

        # Settings related to bullet.
        self.bullet_speed: float
        self.bullet_width: int = 3
        self.bullet_height: int = 15
        self.bullet_color: int = RGB(255, 255, 255)
        self.bullets_allowed: int = 3

        # Settings related to alien ship.
        self.alien_speed: float
        self.fleet_drop_speed: int = 10
        self.fleet_direction: int

        # Settings related to stars.
        self.stars_per_row: int = 10
        self.star_rows: int = 10
        self.stars_speed: float = 0.25

        # Settings related to gameplay.
        self.space_between_aliens: int = 4
        self.speedup_scale: float = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        ''' Initialize settings, which can change dynamically during game. '''
        self.ship_speed = 1.0
        self.bullet_speed = 1.0
        self.alien_speed = 1.0
        self.fleet_direction = 1  # Right movement "1", left movement "-1".

    def reset_stars_speed(self) -> None:
        ''' Reset star speed. Must be done in separate method. '''
        self.stars_speed = 0.25

    def increase_speed(self) -> None:
        ''' Increase gameplay speed. '''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.stars_speed *= self.speedup_scale

    def switch_difficulty(self, mode: int = 1) -> None:
        ''' Choose game difficulty level. '''
        if mode == 1:  # Easy
            self.ship_limit = 3
            self.bullets_allowed = 5
            self.fleet_drop_speed = 10
            self.space_between_aliens = 4
        elif mode == 2:  # Medium
            self.ship_limit = 2
            self.bullets_allowed = 4
            self.fleet_drop_speed = 15
            self.space_between_aliens = 3
        elif mode == 3:  # Hard
            self.ship_limit = 1
            self.bullets_allowed = 3
            self.fleet_drop_speed = 20
            self.space_between_aliens = 2

    def reset_difficulty(self) -> None:
        ''' Reset difficulty level to easy. '''
        self.ship_limit = 3
        self.bullets_allowed = 5
        self.fleet_drop_speed = 10
