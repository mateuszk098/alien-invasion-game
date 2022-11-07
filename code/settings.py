"""
This module provides a Settings object, which is responsible for all gameplay settings.
"""

import pygame as pg


class Settings():
    """Holds all settings of gameplay."""

    def __init__(self) -> None:
        """Initialize settings of game."""
        self.screen_width: int = 1280
        self.screen_height: int = 720
        self.background_color = pg.Color(13, 12, 29)
        self.fps: int = 144
        self.dt: int = 1000 // self.fps

        # Settings related to player's ship and bullets.
        self.player_ships_limit: int = 2
        self.player_ship_speed: float = 0.75*self.dt
        self.player_allowed_bullets: int = 4
        self.player_bullet_speed: float = 0.75*self.dt
        self.player_bullet_points: int = 3

        # Settings related to aliens' ship and bullets.
        self.alien_ship_model: int = 2
        self.alien_ship_speed: float = 0.25*self.dt
        self.alien_allowed_bullets: int = 2
        self.alien_bullet_speed: float = 0.35*self.dt
        self.aliens_fleet_drop_speed: int = 2*self.dt
        self.aliens_fleet_direction: int = 1  # To the right, otherwise -1 to the left.
        self.points_for_alien: int = 50

        # Settings related to aliens' general ship.
        self.aliens_general_ship_model: int = 2
        self.aliens_general_ship_speed: float = 0.5*self.dt
        self.aliens_general_life_points: int = 200

        # Settings related to stars.
        self.stars_per_row: int = 10
        # The game screen is divided into 10 sections, where each of them has 10 stars.
        self.stars_rows: int = 10
        self.star_speed: float = 0.25*self.dt

        # Settings related to gameplay.
        self.space_between_aliens: int = 3
        self.speedup_scale: float = 1.05
        self.score_scale: float = 1.05
        self.final_level: int = 15

    def reset_gameplay_speedup(self) -> None:
        """Resets settings, which can change dynamically during the game."""
        self.player_ship_speed = 0.75*self.dt
        self.player_bullet_speed = 0.75*self.dt
        self.alien_ship_speed = 0.25*self.dt
        self.alien_bullet_speed = 0.35*self.dt
        self.aliens_fleet_direction = 1
        self.points_for_alien = 50
        self.star_speed = 0.25*self.dt
        # Set the default life points is important when we complete the game and launch a new.
        self.aliens_general_life_points = 200

    def increase_gameplay_speed(self) -> None:
        """Increase gameplay speed with each successive level."""
        self.player_ship_speed *= self.speedup_scale
        self.player_bullet_speed *= self.speedup_scale
        self.alien_ship_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale
        self.points_for_alien = int(self.points_for_alien*self.score_scale)
        self.star_speed *= self.speedup_scale

    def switch_difficulty(self, mode: int = 2) -> None:
        """Choose game difficulty level. Default game mode is medium."""
        if mode == 1:  # Easy
            self.player_ships_limit = 3
            self.player_allowed_bullets = 5
            self.player_bullet_points = 4
            self.alien_ship_model = 1
            self.alien_allowed_bullets = 1
            self.aliens_fleet_drop_speed = self.dt
            self.aliens_general_ship_model = 1
            self.space_between_aliens = 4
        elif mode == 2:  # Medium
            self.player_ships_limit = 2
            self.player_allowed_bullets = 4
            self.player_bullet_points = 3
            self.alien_ship_model = 2
            self.alien_allowed_bullets = 2
            self.aliens_fleet_drop_speed = 2*self.dt
            self.aliens_general_ship_model = 2
            self.space_between_aliens = 3
        elif mode == 3:  # Hard
            self.player_ships_limit = 1
            self.player_allowed_bullets = 3
            self.player_bullet_points = 2
            self.alien_ship_model = 3
            self.alien_allowed_bullets = 3
            self.aliens_fleet_drop_speed = 3*self.dt
            self.aliens_general_ship_model = 3
            self.space_between_aliens = 2

    def reset_difficulty(self) -> None:
        """Reset difficulty level to medium."""
        self.player_ships_limit = 2
        self.player_allowed_bullets = 4
        self.player_bullet_points = 2
        self.alien_ship_model = 2
        self.alien_allowed_bullets = 2
        self.aliens_fleet_drop_speed = 2*self.dt
        self.aliens_general_ship_model = 2
        self.space_between_aliens = 3
