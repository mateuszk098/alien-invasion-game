'''
General file with class used to game management.
'''

import sys
from time import sleep

import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.sprite import Group
from pygame.sprite import Sprite

from scoreboard import Scoreboard
from game_stats import GameStats
from spaceship import Spaceship
from settings import Settings
from bullet import Bullet
from alien import Alien
from star import Star
from menu import Menu


class AlienInvasion():
    ''' General class to game management. '''

    __MUSIC_PATH: str = '../sounds/infected_vibes.mp3'

    def __init__(self) -> None:
        ''' Game initialization. '''
        pg.mixer.pre_init(44100, -16, 2, 4096)
        pg.init()
        pg.display.set_caption('Aliens Invasion')
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN])

        pg.mixer.music.load(self.__MUSIC_PATH)
        pg.mixer.music.set_volume(0.25)
        pg.mixer.music.play(-1)

        self.clock = pg.time.Clock()
        self.game_active: bool = False

        self.settings: Settings = Settings()
        self.screen: Surface = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect: Rect = self.screen.get_rect()
        # Full screen.
        # self.screen: Surface = pg.display.set_mode((0, 0), (pg.FULLSCREEN | pg.DOUBLEBUF), 16)
        # self.screen_rect: Rect = self.screen.get_rect()
        # self.settings.screen_width = self.screen_rect.width
        # self.settings.screen_height = self.screen_rect.height

        self.menu: Menu = Menu(self)
        self.stats: GameStats = GameStats(self)
        self.scoreboard: Scoreboard = Scoreboard(self)

        self.player_ship: Spaceship = Spaceship(self)
        self.player_bullets: Group = pg.sprite.Group()

        self.aliens_ships: Group = pg.sprite.Group()
        self.aliens_bullets: Group = pg.sprite.Group()

        self.stars: Group = pg.sprite.Group()
        self._create_stars()

    def run_game(self) -> None:
        ''' Main loop of the game. '''
        while True:
            self.clock.tick(self.settings.fps)
            self._check_events()
            self._update_screen()

    def _check_events(self) -> None:
        ''' Check reaction to button press/release and mouse interaction. '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pg.KEYUP:
                self._check_keyup_events(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                self._check_mouse_events()

    def _check_keydown_events(self, event) -> None:
        ''' Reaction on key press. '''
        if event.key == pg.K_RIGHT:
            self.player_ship.moving_right = True
        if event.key == pg.K_LEFT:
            self.player_ship.moving_left = True
        if event.key == pg.K_g:
            self._start_game()
        if event.key == pg.K_SPACE:
            self._fire_bullet('player')
        if event.key == pg.K_r:
            self._reset_game()
        if event.key == pg.K_s:
            self.menu.show_settings()
        if event.key == pg.K_1:
            self.menu.switch_to_easy_mode()
        if event.key == pg.K_2:
            self.menu.switch_to_medium_mode()
        if event.key == pg.K_3:
            self.menu.switch_to_hard_mode()
        if event.key == pg.K_h:
            self.menu.show_help()
        if event.key == pg.K_ESCAPE:
            self.menu.return_to_menu()
        if event.key == pg.K_q:
            sys.exit()

    def _check_keyup_events(self, event) -> None:
        ''' Reaction on key release. '''
        if event.key == pg.K_RIGHT:
            self.player_ship.moving_right = False
        if event.key == pg.K_LEFT:
            self.player_ship.moving_left = False

    def _check_mouse_events(self) -> None:
        ''' Reaction to mouse click. '''
        if not self.game_active:
            mouse_pos: tuple[int, int] = pg.mouse.get_pos()
            if self.menu.check_play_button(mouse_pos):
                self._start_game()
            if self.menu.check_exit_button(mouse_pos):
                sys.exit()
            if self.menu.check_help_button(mouse_pos):
                self.menu.show_help()
            if self.menu.check_easy_button(mouse_pos):
                self.menu.switch_to_easy_mode()
            if self.menu.check_medium_button(mouse_pos):
                self.menu.switch_to_medium_mode()
            if self.menu.check_hard_button(mouse_pos):
                self.menu.switch_to_hard_mode()
            if self.menu.check_settings_button(mouse_pos):
                self.menu.show_settings()
            if self.menu.check_exit_from_settings(mouse_pos):
                self.menu.return_to_menu()

    def _start_game(self) -> None:
        ''' 
        Resets current statistics, prepares scoreboard
        and aliens fleet and starts the game.
        '''
        if not self.game_active:  # Due to the possibility of "g" press.
            self.stats.reset_stats()
            self.scoreboard.prepare_current_score()
            self.scoreboard.prepare_current_level()
            self.scoreboard.prepare_remaining_player_ships()
            self.player_ship.centre_spaceship()
            self._create_fleet()
            pg.mouse.set_visible(False)
            self.game_active = True

    def _reset_game(self) -> None:
        ''' 
        Resets the current game, remove the remaining bullets and aliens,
        set the player's ship to the screen centre, set the star's speed
        to default, and return to the menu.
        '''
        if self.game_active:
            self.player_bullets.empty()
            self.aliens_bullets.empty()
            self.aliens_ships.empty()
            self.player_ship.centre_spaceship()
            self.settings.reset_gameplay_speedup()
            self.menu.return_to_menu()
            pg.mouse.set_visible(True)
            self.game_active = False

    def _fire_bullet(self, owner: str) -> None:
        ''' 
        If possible, create a new player's or alien's bullet
        and add it to the appropriate group. 
        '''
        if self.game_active:
            # Fire player's bullet.
            if len(self.player_bullets) < self.settings.player_allowed_bullets and owner == 'player':
                player_bullet: Bullet = Bullet(self, owner)
                player_bullet.fire_sound.play()
                self.player_bullets.add(player_bullet)
            # Fire alien's bullet.
            if len(self.aliens_bullets) < self.settings.alien_allowed_bullets and owner == 'alien':
                alien_bullet: Bullet = Bullet(self, owner)
                self.aliens_bullets.add(alien_bullet)

    def _update_bullets(self) -> None:
        ''' 
        Updates player's and aliens' bullets position and remove them
        if any of the bullets are out of the screen.
        '''
        self.player_bullets.update()
        self.aliens_bullets.update()

        for player_bullet in self.player_bullets.copy():
            if player_bullet.rect.bottom <= 0:  # type: ignore
                self.player_bullets.remove(player_bullet)

        for alien_bullet in self.aliens_bullets.copy():
            if alien_bullet.rect.top >= self.screen_rect.bottom:  # type: ignore
                self.aliens_bullets.remove(alien_bullet)

        self._check_collisions()

    def _check_collisions(self) -> None:
        '''
        Checks collisions between the player's and aliens' bullets and between
        the player's bullets and aliens' ships. It is responsible for game score
        calculation after shooting the alien ship and for game speedup if we have
        shot every alien.
        '''
        # Create a new fleet with a gameplay speedup.
        if not self.aliens_ships:
            self.player_bullets.empty()
            self.aliens_bullets.empty()
            self.settings.increase_gameplay_speed()
            self.stats.current_level += 1
            self.scoreboard.prepare_current_level()
            self._create_fleet()

        player_bullet_and_alien_ship: dict[Sprite, Sprite] = pg.sprite.groupcollide(
            self.player_bullets, self.aliens_ships, True, True)  # True means to remove object.

        player_bullet_and_alien_bullet: dict[Sprite, Sprite] = pg.sprite.groupcollide(
            self.player_bullets, self.aliens_bullets, True, True)

        # Collision between alien's bullet and player's spaceship.
        if pg.sprite.spritecollideany(self.player_ship, self.aliens_bullets) is not None:
            self._ship_hit()

        if player_bullet_and_alien_ship:
            # Count every alien if player's bullet hit several aliens.
            for aliens in player_bullet_and_alien_ship.values():
                self.stats.current_score += self.settings.points_for_alien*len(aliens)  # type: ignore

            self.scoreboard.prepare_current_score()
            self.scoreboard.check_the_highest_score()

    def _create_fleet(self) -> None:
        '''
        Creates new aliens' fleet considering available screen width,
        screen height, screen margin and space between aliens.
        '''
        alien: Alien = Alien(self)
        space: int = self.settings.space_between_aliens

        alien_width: int = alien.rect.width
        available_space_x: int = self.settings.screen_width - (4*alien_width)
        number_aliens_x: int = available_space_x // (space*alien_width)

        alien_height: int = alien.rect.height
        available_space_y: int = self.settings.screen_height // 2
        number_rows: int = available_space_y // (2*alien_height)

        # Create the fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number: int, row_number: int) -> None:
        '''
        Create a new alien ship in the specified (x,y) position and add
        it to the appropriate group. 
        '''
        alien: Alien = Alien(self)
        space: int = self.settings.space_between_aliens
        alien_width: int = alien.rect.width
        alien_height: int = alien.rect.height
        alien.x = alien_width + space*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = 2*alien.rect.height + 2*alien_height*row_number
        self.aliens_ships.add(alien)

    def _update_aliens(self) -> None:
        '''
        Updates all aliens' ships' positions on the screen and checks if there 
        is a collision between them and the player's ship or if any aliens 
        arrive at the screen's bottom edge. 
        '''
        self._check_fleet_edges()
        self.aliens_ships.update()

        # Check collision between player's spaceship and alien's ship.
        if pg.sprite.spritecollideany(self.player_ship, self.aliens_ships):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self) -> None:
        ''' Change the fleet movement's direction if any alien comes to the screen edge. '''
        for alien in self.aliens_ships.sprites():
            if alien.check_left_right_screen_edge() is True:  # type: ignore
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        ''' Shifts the whole alien fleet and changes the direction of its movement. '''
        for alien in self.aliens_ships.sprites():
            alien.rect.y += self.settings.aliens_fleet_drop_speed  # type: ignore
        self.settings.aliens_fleet_direction *= -1

    def _check_aliens_bottom(self) -> None:
        ''' We lose the current round if any aliens arrive at the screen's bottom edge. '''
        for alien in self.aliens_ships.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:  # type: ignore
                self._ship_hit()
                break

    def _ship_hit(self) -> None:
        '''
        If the player's ship has been hit, remove the remaining bullets
        and aliens, set the ship to the screen centre, and start a new
        round if the player has remaining ships.
        '''
        self.aliens_ships.empty()
        self.aliens_bullets.empty()
        self.player_bullets.empty()
        self.player_ship.centre_spaceship()

        if self.stats.remaining_player_ships > 0:
            self.stats.remaining_player_ships -= 1
            self.scoreboard.prepare_remaining_player_ships()
            self._create_fleet()
        else:
            self.settings.reset_gameplay_speedup()
            self.menu.return_to_menu()
            pg.mouse.set_visible(True)
            self.game_active = False

        sleep(1.0)

    def _create_stars(self) -> None:
        ''' Creates outer space with a constant number of stars in the current frame. '''
        pixels_per_row: int = self.settings.screen_height // self.settings.stars_rows

        for row in range(self.settings.stars_rows):
            for _ in range(self.settings.stars_per_row):
                star: Star = Star(self)
                star.y += pixels_per_row*row
                star.rect.y = int(star.y)
                self.stars.add(star)

    def _update_stars(self) -> None:
        ''' 
        Updates all stars' positions, which causes the feeling of
        traversing space. If any stars arrive beyond the screen's bottom
        edge, they are removed, and a new star is created.
        '''
        self.stars.update()

        for star in self.stars.copy():
            if star.rect.top > self.screen_rect.bottom:  # type: ignore
                self.stars.remove(star)

        pixels_per_row: int = self.settings.screen_height // self.settings.stars_rows

        # Add new star.
        if len(self.stars) < self.settings.stars_per_row*self.settings.stars_rows:
            new_star: Star = Star(self)
            # Provides effect that stars coming on the screen naturally.
            new_star.y -= pixels_per_row
            new_star.rect.y = int(new_star.y)
            self.stars.add(new_star)

    def _update_screen(self) -> None:
        ''' Updates the game screen. '''
        self.screen.fill(self.settings.background_color)
        self._update_stars()
        self.stars.draw(self.screen)
        self.player_ship.draw_spaceship()

        if self.game_active is True:
            self.scoreboard.show_scoreboard_and_stats()
            self.player_ship.update()
            self._update_aliens()
            self.aliens_ships.draw(self.screen)
            self._fire_bullet('alien')
            self._update_bullets()

            for player_bullet in self.player_bullets.sprites():
                player_bullet.draw_bullet()  # type: ignore
            for alien_bullet in self.aliens_bullets.sprites():
                alien_bullet.draw_bullet()  # type: ignore
        else:
            self.menu.draw_menu()

        pg.display.flip()  # Update of the screen.

        # print(f"Ship Speed: {self.settings.player_ship_speed:.1f}, Player Bullet Speed: {self.settings.player_bullet_speed:.1f}, Alien Ship Speed: {self.settings.alien_ship_speed:.1f}, Alien Bullet Speed: {self.settings.alien_bullet_speed:.1f}, Points: {self.settings.points_for_alien:.1f}, Stars Speed: {self.settings.star_speed:.1f}")

        # print(f"Ships: {self.settings.player_ships_limit}, Player Bullets: {self.settings.player_allowed_bullets}, Alien Bullets: {self.settings.alien_allowed_bullets}, Drop Speed: {self.settings.aliens_fleet_drop_speed}")

        # print(f"Stars: {len(self.stars)}, Aliens: {len(self.aliens_ships)}, Bullets: {len(self.player_bullets)}, Alien Bullets: {len(self.aliens_bullets)},")
