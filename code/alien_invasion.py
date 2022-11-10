"""
This module provides an AlienInvasion class. The AlienInvasion object 
is responsible for the gameplay implementation and uses all other modules. 
"""

import sys
from time import sleep
from random import randint

import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.sprite import Sprite

from bullet import PlayerBullet, AlienSoldierBullet, AlienGeneralBullet
from alien import AlienSoldier, AlienGeneral
from scoreboard import Scoreboard
from game_stats import GameStats
from spaceship import Spaceship
from settings import Settings
from star import Star
from menu import Menu


class AlienInvasion():
    """The AlienInvasion class provides a general game management."""

    __MUSIC_PATH: str = '../sounds/infected_vibes.mp3'

    def __init__(self) -> None:
        """Game initialisation."""
        pg.mixer.pre_init(44100, -16, 2, 4096)
        pg.init()
        pg.display.set_caption('Aliens Invasion')
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN])
        self.clock = pg.time.Clock()

        pg.mixer.music.load(self.__MUSIC_PATH)
        pg.mixer.music.set_volume(0.2)
        # pg.mixer.music.play(-1)

        # Primary states of the game.
        self.game_active: bool = False
        self.game_paused: bool = False
        self.game_complete: bool = False
        self.final_level_achieved: bool = False

        self.settings: Settings = Settings()
        # self.screen: Surface = pg.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))
        # self.screen_rect: Rect = self.screen.get_rect()
        # Full screen.
        self.screen: Surface = pg.display.set_mode((0, 0), (pg.FULLSCREEN | pg.DOUBLEBUF), 16)
        self.screen_rect: Rect = self.screen.get_rect()
        self.settings.screen_width = self.screen_rect.width
        self.settings.screen_height = self.screen_rect.height

        self.menu: Menu = Menu(self)
        self.stats: GameStats = GameStats(self)
        self.scoreboard: Scoreboard = Scoreboard(self)

        self.player_ship: Spaceship = Spaceship(self)
        self.player_bullets = pg.sprite.Group()

        self.alien_soldier_ships = pg.sprite.Group()
        self.alien_soldier_bullets = pg.sprite.Group()
        self.alien_general_bullets = pg.sprite.Group()

        self.stars = pg.sprite.Group()
        self._create_stars()

    def run_game(self) -> None:
        """Main loop of the game."""
        while True:
            self.clock.tick(self.settings.FPS)
            self._check_events()
            self._update_screen()

    def _check_events(self) -> None:
        """Check reaction to button press/release and mouse interaction."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self._check_mouse_events()

    def _check_keydown_events(self, event) -> None:
        """Reactions on key press."""
        if event.key == pg.K_RIGHT:
            self.player_ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.player_ship.moving_left = True
        elif event.key == pg.K_g:
            self._start_game()
        elif event.key == pg.K_SPACE:
            self._fire_bullet("Player")
        elif event.key == pg.K_r:
            self._reset_game()
        elif event.key == pg.K_s:
            self.menu.show_settings()
        elif event.key == pg.K_1:
            self.menu.switch_to_easy_mode()
        elif event.key == pg.K_2:
            self.menu.switch_to_medium_mode()
        elif event.key == pg.K_3:
            self.menu.switch_to_hard_mode()
        elif event.key == pg.K_h:
            self.menu.show_help()
        elif event.key == pg.K_ESCAPE:
            self.menu.return_to_menu()
            self.game_complete = False
        elif event.key == pg.K_q:
            sys.exit()
        elif event.key == pg.K_p:
            self._pause_game()

    def _check_keyup_events(self, event) -> None:
        """Reactions on key release."""
        if event.key == pg.K_RIGHT:
            self.player_ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.player_ship.moving_left = False

    def _check_mouse_events(self) -> None:
        """Reactions to mouse click."""
        if not self.game_active:
            mouse_pos: tuple[int, int] = pg.mouse.get_pos()
            if self.menu.check_button_press(mouse_pos, "Play"):
                self._start_game()
            elif self.menu.check_button_press(mouse_pos, "Exit Game"):
                sys.exit()
            elif self.menu.check_button_press(mouse_pos, "Help"):
                self.menu.show_help()
            elif self.menu.check_button_press(mouse_pos, "Easy Mode"):
                self.menu.switch_to_easy_mode()
            elif self.menu.check_button_press(mouse_pos, "Medium Mode"):
                self.menu.switch_to_medium_mode()
            elif self.menu.check_button_press(mouse_pos, "Hard Mode"):
                self.menu.switch_to_hard_mode()
            elif self.menu.check_button_press(mouse_pos, "Settings"):
                self.menu.show_settings()
            elif self.menu.check_button_press(mouse_pos, "Back"):
                self.menu.return_to_menu()

    def _start_game(self) -> None:
        """Resets current game statistics, prepares scoreboard, alien fleet and starts the game."""
        if not self.game_active and not self.game_complete:
            self.stats.reset_stats()
            self.scoreboard.prepare_current_score()
            self.scoreboard.prepare_current_level()
            self.scoreboard.prepare_remaining_player_ships()
            self.player_ship.set_center()
            self._create_alien_soldiers_fleet()
            self.game_active = True
            pg.mouse.set_visible(False)

    def _reset_game(self) -> None:
        """
        Resets the current game, removes the remaining bullets and aliens,
        set the player's ship to the screen centre, set the star's speed
        to default, and return to the menu.
        """
        if self.game_active and not self.game_paused:
            self.player_bullets.empty()
            self.alien_soldier_bullets.empty()
            self.alien_general_bullets.empty()
            self.alien_soldier_ships.empty()
            self.player_ship.set_center()
            self.settings.reset_gameplay_speedup()
            self.menu.return_to_menu()
            self.game_active = False
            self.final_level_achieved = False
            pg.mouse.set_visible(True)

    def _pause_game(self) -> None:
        """Pause the game if the gameplay is active."""
        if self.game_active:
            self.game_paused = not self.game_paused

    def _create_stars(self) -> None:
        """Creates outer space with a constant number of stars."""
        row_space: int = self.settings.screen_height // self.settings.stars_rows
        for row in range(self.settings.stars_rows):
            for _ in range(self.settings.stars_per_row):
                star: Star = Star(self)
                star.y += row_space*row
                star.rect.y = int(star.y)
                self.stars.add(star)

    def _update_stars(self) -> None:
        """
        Updates all stars' positions, which causes the feeling of
        traversing space. If any stars arrive beyond the screen's bottom
        edge, they are removed, and new stars are created.
        """
        self.stars.update()

        for star in self.stars.copy():
            if star.rect.top > self.screen_rect.bottom:  # type: ignore
                self.stars.remove(star)

        row_space: int = self.settings.screen_height // self.settings.stars_rows
        # Provide constant number of stars.
        if len(self.stars) < self.settings.stars_per_row*self.settings.stars_rows:
            new_star: Star = Star(self)
            new_star.y -= row_space  # Provides effect that stars coming on the screen naturally.
            new_star.rect.y = int(new_star.y)
            self.stars.add(new_star)

    def _fire_bullet(self, owner: str) -> None:
        """Adds a new Bullet object to the appropriate group."""
        if owner == "Player":
            if self.game_active and len(self.player_bullets) < self.settings.player_allowed_bullets:
                player_bullet: PlayerBullet = PlayerBullet(self)
                # player_bullet.play_sound()
                self.player_bullets.add(player_bullet)
        elif owner == "AlienSoldier":
            if self.alien_soldier_ships and len(self.alien_soldier_bullets) < self.settings.alien_allowed_bullets:
                self.alien_soldier_bullets.add(AlienSoldierBullet(self))
        elif owner == "AlienGeneral":
            if randint(1, 1000) <= 10 and len(self.alien_general_bullets) < self.settings.alien_general_allowed_bullets:
                self.alien_general_bullets.add(AlienGeneralBullet(self))

    def _update_bullets(self) -> None:
        """Updates bullets positions and remove them if any bullets are out of the screen."""
        self.player_bullets.update()
        self.alien_soldier_bullets.update()
        self.alien_general_bullets.update()

        for player_bullet in self.player_bullets.copy():
            if player_bullet.rect.bottom <= 0:  # type: ignore
                self.player_bullets.remove(player_bullet)

        for alien_bullet in self.alien_soldier_bullets.copy():
            if alien_bullet.rect.top >= self.screen_rect.bottom:  # type: ignore
                self.alien_soldier_bullets.remove(alien_bullet)

        for general_bullet in self.alien_general_bullets.copy():
            if general_bullet.rect.top >= self.screen_rect.bottom:  # type: ignore
                self.alien_general_bullets.remove(general_bullet)

        self._check_collisions()

    def _check_collisions(self) -> None:
        """
        The primary method. Checks collisions between bullets, the player's spaceship and 
        aliens' ships. It is responsible for the game score calculation after shooting the 
        alien ship and for game speedup if each alien is killed. If the player reaches the 
        final level, the alien general is created. The game ends when the player kills the 
        generalship.
        """
        # Prepare the usual level - create a new soldiers fleet with a gameplay speedup.
        if not self.alien_soldier_ships and not self.final_level_achieved:
            self.player_bullets.empty()
            self.alien_soldier_bullets.empty()
            self.settings.increase_gameplay_speed()
            self._create_alien_soldiers_fleet()
            self.stats.current_level += 1
            self.scoreboard.prepare_current_level()

        # Check the collision between the player's bullets and the alien's bullets.
        # True means to remove object.
        pg.sprite.groupcollide(self.player_bullets, self.alien_soldier_bullets, True, True)

        # Check the collision between the player's spaceship and the alien's bullets.
        if pg.sprite.spritecollideany(self.player_ship, self.alien_soldier_bullets):
            self._ship_hit()

        # Check the collision between the player's bullets and the alien's ships.
        player_bullet_and_alien_ship: dict[Sprite, Sprite] = pg.sprite.groupcollide(
            self.player_bullets, self.alien_soldier_ships, True, True)

        if player_bullet_and_alien_ship:
            # Count points for every alien if the player's bullet hits several aliens at once.
            for aliens in player_bullet_and_alien_ship.values():
                self.stats.current_score += self.settings.points_for_alien*len(aliens)  # type: ignore
            self.scoreboard.prepare_current_score()
            self.scoreboard.check_the_highest_score()

        # Prepare the final level - create the alien general.
        if not self.final_level_achieved and self.stats.current_level == self.settings.final_level:
            self.alien_soldier_ships.empty()
            self.alien_general_ship: AlienGeneral = AlienGeneral(self)
            self.final_level_achieved = True

        if self.final_level_achieved:
            # Check the collision between the player's bullets and the alien general ship.
            for player_bullet in self.player_bullets.copy():
                if pg.sprite.collide_rect(self.alien_general_ship, player_bullet):
                    self.player_bullets.remove(player_bullet)
                    self.alien_general_ship.life_points -= self.settings.player_bullet_points
                if self.alien_general_ship.life_points <= 0:
                    self.game_complete = True
                    self._reset_game()
            # Check the collision between the player's bullets and the alien general bullets.
            pg.sprite.groupcollide(self.player_bullets, self.alien_general_bullets, True, True)
            # Check the collision between the player's spaceship and the alien general bullets.
            if pg.sprite.spritecollideany(self.player_ship, self.alien_general_bullets):
                self._ship_hit()

    def _create_alien_soldiers_fleet(self) -> None:
        """
        Creates new aliens' fleet considering available screen width,
        screen height, screen margin and space between aliens.
        """
        alien: AlienSoldier = AlienSoldier(self)
        space: int = self.settings.space_between_aliens

        alien_width: int = alien.rect.width
        available_space_x: int = 2*self.settings.screen_width // 3
        number_aliens_x: int = available_space_x // (space*alien_width)

        alien_height: int = alien.rect.height
        available_space_y: int = self.settings.screen_height // 3
        number_rows: int = available_space_y // (3*alien_height // 2)

        # Create the fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien_soldier(alien_number, row_number)

    def _create_alien_soldier(self, alien_number: int, row_number: int) -> None:
        """Create a new alien ship in the specified (x,y) position and add it to the appropriate group."""
        alien: AlienSoldier = AlienSoldier(self)
        space: int = self.settings.space_between_aliens
        alien_width: int = alien.rect.width
        alien_height: int = alien.rect.height
        alien.x = alien_width + space*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = 3*alien.rect.height + (3*alien_height*row_number // 2)
        self.alien_soldier_ships.add(alien)

    def _update_alien_soldiers(self) -> None:
        """
        Updates all aliens' ships' positions on the screen and checks if there
        is a collision between them and the player's spaceship or if any aliens
        arrive at the screen's bottom edge.
        """
        self._check_screen_edge_for_soldiers()
        self.alien_soldier_ships.update()

        if pg.sprite.spritecollideany(self.player_ship, self.alien_soldier_ships):
            self._ship_hit()

        self._check_any_soldier_reaches_screen_bottom()

    def _update_alien_general(self) -> None:
        """Updates aliens' general ship position and its movement direction."""
        if self.alien_general_ship.check_left_right_screen_edge():
            self.settings.alien_moving_direction *= -1
        self.alien_general_ship.update()

    def _check_screen_edge_for_soldiers(self) -> None:
        """Change the soldiers fleet movement's direction if any aliens come to the screen edge."""
        for alien in self.alien_soldier_ships:
            if alien.check_left_right_screen_edge():  # type: ignore
                self._change_soldiers_fleet_direction()
                break

    def _change_soldiers_fleet_direction(self) -> None:
        """Shifts the whole alien soldiers fleet and changes the direction of its movement. """
        for alien in self.alien_soldier_ships:
            alien.rect.y += self.settings.alien_drop_shift_speed  # type: ignore
        self.settings.alien_moving_direction *= -1

    def _check_any_soldier_reaches_screen_bottom(self) -> None:
        """We lose the current game round if any aliens arrive at the bottom edge of the screen."""
        for alien in self.alien_soldier_ships:
            if alien.rect.bottom >= self.screen_rect.bottom:  # type: ignore
                self._ship_hit()
                break

    def _ship_hit(self) -> None:
        """
        If the player's spaceship has been hit, remove the remaining bullets
        and aliens, set the spaceship to the screen centre, and start a new
        round if the player has remaining lives.
        """
        self.alien_soldier_ships.empty()
        self.alien_soldier_bullets.empty()
        self.alien_general_bullets.empty()
        self.player_bullets.empty()
        self.player_ship.set_center()

        if self.stats.remaining_player_ships > 0:
            self.stats.remaining_player_ships -= 1
            self.scoreboard.prepare_remaining_player_ships()
            if not self.final_level_achieved:
                self._create_alien_soldiers_fleet()
            else:
                self.alien_general_ship.reset_alien_general_ship()
        else:
            self.settings.reset_gameplay_speedup()
            self.menu.return_to_menu()
            pg.mouse.set_visible(True)
            self.game_active = False
            self.final_level_achieved = False

        sleep(1.0)

    def _update_active_game(self) -> None:
        """Updates and draws gameplay objects when the game is active."""
        self.scoreboard.show_scoreboard_and_stats()

        self._update_bullets()
        self.player_ship.update()
        self.player_ship.draw()
        self.player_bullets.draw(self.screen)

        if not self.final_level_achieved:
            self._update_alien_soldiers()
            self.alien_soldier_ships.draw(self.screen)
            self.alien_soldier_bullets.draw(self.screen)
            self._fire_bullet("AlienSoldier")
        else:
            self._update_alien_general()
            self.alien_general_ship.draw()
            self.alien_general_bullets.draw(self.screen)
            self._fire_bullet("AlienGeneral")

    def _update_screen(self) -> None:
        """Updates the game screen."""
        self.screen.fill(self.settings.background_color)
        self._update_stars()
        self.stars.draw(self.screen)

        if self.game_complete:
            self.menu.draw_message("Congratulations", ypos=250)
        elif self.game_paused:
            self.menu.draw_message("Pause", fontsize=128)
        elif self.game_active:
            self._update_active_game()
        else:
            self.player_ship.draw()
            self.menu.draw_menu()

        pg.display.flip()  # Update of the screen.
