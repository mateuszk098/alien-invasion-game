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
        self.ship_speed: float = 1.5

        # Settings related to bullet.
        self.bullet_speed: float = 1.0
        self.bullet_width: int = 3
        self.bullet_height: int = 15
        self.bullet_color: int = RGB(255, 255, 255)
        self.bullets_allowed: int = 3

        # Settings related to alien ship
        self.alien_speed: float = 1.0
        self.fleet_drop_speed: int = 10
        self.fleet_direction: int = 1  # Right movement "1", left movement "-1"

        # Settings related to star
        self.stars_per_row: int = 10
        self.star_rows: int = 10
        self.stars_speed: float = 0.25
