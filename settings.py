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
        self.background_color: int = RGB(230, 230, 230)

        # Settings related to spaceship.
        self.ship_speed: float = 1.5

        # Settings related to bullet.
        self.bullet_speed: float = 1.0
        self.bullet_width: int = 3
        self.bullet_height: int = 15
        self.bullet_color: int = RGB(60, 60, 60)
        self.bullets_allowed: int = 3
