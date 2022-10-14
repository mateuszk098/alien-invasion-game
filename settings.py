'''
General file to game settings management.
'''

from ctypes.wintypes import RGB


class Settings():
    ''' Holds all settings of game. '''

    def __init__(self) -> None:
        ''' Initialize settings of game. '''
        self.screen_width: int = 1280
        self.screen_height: int = 720
        self.background_color: int = RGB(230, 230, 230)
