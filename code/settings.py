'''
General file to game settings management.
'''


class Settings():
    ''' Holds all settings of game. '''

    # Settings related to gameplay.
    ship_speed: float
    bullet_speed: float
    alien_speed: float
    fleet_direction: int

    def __init__(self) -> None:
        ''' Initialize settings of game. '''
        # Settings related to game screen.
        self.screen_width: int = 1280
        self.screen_height: int = 720
        self.background_color: tuple[int, int, int] = (13, 12, 29)
        self.fps: int = 144
        self.dt: int = 1000//self.fps

        # Settings related to spaceship.
        self.ship_limit: int = 2

        # Settings related to bullet.
        self.player_allowed_bullets: int = 4
        self.aliens_allowed_bullets: int = 1

        # Settings related to alien ship.
        self.fleet_drop_speed: int = 2*self.dt
        self.alien_points: int = 50

        # Settings related to stars.
        self.stars_per_row: int = 10
        self.star_rows: int = 10
        self.stars_speed: float = 0.25*self.dt

        # Settings related to gameplay.
        self.space_between_aliens: int = 3
        self.speedup_scale: float = 1.05
        self.score_scale: float = 1.05
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        ''' Initialize settings, which can change dynamically during game. '''
        self.ship_speed = 0.75*self.dt
        self.bullet_speed = 0.75*self.dt
        self.alien_speed = 0.25*self.dt
        self.fleet_direction = 1  # Right movement "1", left movement "-1".

    def increase_speed(self) -> None:
        ''' Increase gameplay speed. '''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.stars_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)

    def reset_stars_speed(self) -> None:
        ''' Reset star speed. Must be done in separate method. '''
        self.stars_speed = 0.25*self.dt

    def switch_difficulty(self, mode: int = 2) -> None:
        ''' Choose game difficulty level. '''
        if mode == 1:  # Easy
            self.ship_limit = 3
            self.player_allowed_bullets = 5
            self.fleet_drop_speed = self.dt
            self.space_between_aliens = 4
        elif mode == 2:  # Medium
            self.ship_limit = 2
            self.player_allowed_bullets = 4
            self.fleet_drop_speed = 2*self.dt
            self.space_between_aliens = 3
        elif mode == 3:  # Hard
            self.ship_limit = 1
            self.player_allowed_bullets = 3
            self.fleet_drop_speed = 3*self.dt
            self.space_between_aliens = 2

    def reset_difficulty(self) -> None:
        ''' Reset difficulty level to medium. '''
        self.ship_limit = 2
        self.player_allowed_bullets = 4
        self.fleet_drop_speed = 2*self.dt
        self.space_between_aliens = 3
