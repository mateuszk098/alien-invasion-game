"""
This module provides a Settings object responsible for the most important game settings. 
"""

import pygame as pg


class Settings():
    """Holds all most important settings of the game."""

    def __init__(self) -> None:
        """Initialise Settings object."""
        self.screen_width: int = 1280
        self.screen_height: int = 720
        self.background_color = pg.Color("#0d0c1d")
        self.text_color = pg.Color("#f0f0f0")
        self.button_released_background_color = pg.Color("#154360")
        self.button_pressed_background_color = pg.Color("#60ce80")

        self.FPS: int = 144
        self._DT: int = 1000 // self.FPS

        self.player_ships_limit: int = 2
        self.player_ship_speed: float = 0.75*self._DT
        self.player_allowed_bullets: int = 4
        self.player_bullet_speed: float = 0.75*self._DT
        self.player_bullet_points: int = 3

        self.alien_ship_model: int = 2
        self.alien_ship_speed: float = 0.25*self._DT
        self.alien_allowed_bullets: int = 2
        self.alien_bullet_speed: float = 0.35*self._DT
        self.alien_drop_shift_speed: int = 4*self._DT
        self.alien_moving_direction: int = 1  # To the right, otherwise -1 to the left.
        self.points_for_alien: int = 50

        self.alien_general_ship_model: int = 2
        self.alien_general_ship_speed: float = 0.5*self._DT
        self.alien_general_allowed_bullets: int = 4
        self.alien_general_life_points: int = 200
        self.alien_general_life_bar_color = pg.Color("#ea3c53")
        self.alien_general_life_bar_outline_color = pg.Color("#7c0a02")

        # The game screen is divided into 10 sections, each with 10 stars.
        self.stars_per_row: int = 10
        self.stars_rows: int = 10
        self.star_speed: float = 0.25*self._DT

        # Settings related to the gameplay.
        self.space_between_aliens: int = 50
        self.additional_alien_in_row: int = 1
        self.speedup_scale: float = 1.05
        self.score_scale: float = 1.05
        self.final_level: int = 15

    def reset_alien_moving_direction(self) -> None:
        """Set the alien_moving_direction to 1 (right)."""
        self.alien_moving_direction = 1

    def reset_gameplay_speedup(self) -> None:
        """Resets settings, which change dynamically during the game."""
        self.player_ship_speed = 0.75*self._DT
        self.player_bullet_speed = 0.75*self._DT
        self.alien_ship_speed = 0.25*self._DT
        self.alien_bullet_speed = 0.35*self._DT
        self.alien_moving_direction = 1
        self.points_for_alien = 50
        self.star_speed = 0.25*self._DT

    def increase_gameplay_speed(self) -> None:
        """Increase gameplay speed with each successive level."""
        self.player_ship_speed *= self.speedup_scale
        self.player_bullet_speed *= self.speedup_scale
        self.alien_ship_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale
        self.points_for_alien = int(self.points_for_alien*self.score_scale)
        self.star_speed *= self.speedup_scale

    def switch_difficulty(self, mode: int) -> None:
        """Choose game difficulty mode. The default game mode is medium."""
        if mode == 1:  # Easy
            self.player_ships_limit = 3
            self.player_allowed_bullets = 5
            self.player_bullet_points = 4
            self.alien_ship_model = 1
            self.alien_allowed_bullets = 1
            self.alien_drop_shift_speed = 3*self._DT
            self.alien_general_ship_model = 1
            self.alien_general_allowed_bullets = 3
            self.additional_alien_in_row = 0
        elif mode == 2:  # Medium
            self.player_ships_limit = 2
            self.player_allowed_bullets = 4
            self.player_bullet_points = 3
            self.alien_ship_model = 2
            self.alien_allowed_bullets = 2
            self.alien_drop_shift_speed = 4*self._DT
            self.alien_general_ship_model = 2
            self.alien_general_allowed_bullets = 4
            self.additional_alien_in_row = 1
        elif mode == 3:  # Hard
            self.player_ships_limit = 1
            self.player_allowed_bullets = 3
            self.player_bullet_points = 2
            self.alien_ship_model = 3
            self.alien_allowed_bullets = 3
            self.alien_drop_shift_speed = 5*self._DT
            self.alien_general_ship_model = 3
            self.alien_general_allowed_bullets = 5
            self.additional_alien_in_row = 2

    def reset_difficulty(self) -> None:
        """Resets the game difficulty mode to medium."""
        self.player_ships_limit = 2
        self.player_allowed_bullets = 4
        self.player_bullet_points = 2
        self.alien_ship_model = 2
        self.alien_allowed_bullets = 2
        self.alien_drop_shift_speed = 4*self._DT
        self.alien_general_ship_model = 2
        self.alien_general_allowed_bullets = 4
        self.additional_alien_in_row = 1
