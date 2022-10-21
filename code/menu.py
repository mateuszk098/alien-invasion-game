''' 
General file with menu management.
'''

from button import Button


class Menu():

    def __init__(self, ai_game) -> None:
        ''' Initialize menu buttons in the game. '''
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.play_button: Button = Button(ai_game, 'Play', -50)
        self.settings_button: Button = Button(ai_game, 'Settings', 25)

        self.easy_mode_button: Button = Button(ai_game, 'Easy Mode', -125)
        self.medium_mode_button: Button = Button(ai_game, 'Medium Mode', -50)
        self.hard_mode_button: Button = Button(ai_game, 'Hard Mode', 25)
        self.back_button: Button = Button(ai_game, 'Back', 100)

        self.menu_visible: bool = True
        self.settings_visible: bool = False
        self.easy_clicked: bool = False
        self.medium_clicked: bool = False
        self.hard_clicked: bool = False

    def draw_menu(self) -> None:
        ''' Display the menu/settings on the screen. '''
        if self.menu_visible is True:
            self.play_button.draw_button()
            self.settings_button.draw_button()

        if self.settings_visible is True:
            self.easy_mode_button.draw_button(self.easy_clicked)
            self.medium_mode_button.draw_button(self.medium_clicked)
            self.hard_mode_button.draw_button(self.hard_clicked)
            self.back_button.draw_button()

    def check_play_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the play button is clicked by mouse. '''
        button_clicked: bool = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked is True and self.menu_visible is True:
            return True
        return False

    def check_settings_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the settings button is clicked by mouse. '''
        button_clicked: bool = self.settings_button.rect.collidepoint(mouse_pos)
        if button_clicked is True and self.settings_visible is False:
            return True
        return False

    def enter_settings(self) -> None:
        ''' Changes flags related to enter settings. '''
        self.menu_visible = False
        self.settings_visible = True
        self.stats.settings_active = True

    def exit_settings(self) -> None:
        ''' Changes flags related to exit settings. '''
        self.menu_visible = True
        self.settings_visible = False
        self.stats.settings_active = False

    def reset_mode_buttons(self) -> None:
        ''' Reset difficulty buttons to default. '''
        self.easy_clicked = False
        self.medium_clicked = False
        self.hard_clicked = False

    def game_mode_management(self, mouse_pos: tuple[int, int]) -> None:
        ''' Management of game difficulty mode. '''
        easy_clicked: bool = self.easy_mode_button.rect.collidepoint(mouse_pos)
        medium_clicked: bool = self.medium_mode_button.rect.collidepoint(mouse_pos)
        hard_clicked: bool = self.hard_mode_button.rect.collidepoint(mouse_pos)
        back_clicked: bool = self.back_button.rect.collidepoint(mouse_pos)

        # Check if mode has been changed, otherwise exit settings.
        self._switch_mode(easy_clicked, medium_clicked, hard_clicked)
        self._check_back_button(back_clicked)

    def _check_back_button(self, back_clicked) -> None:
        ''' Checks if the back button is clicked by mouse. '''
        if back_clicked is True:
            self.exit_settings()

    def _switch_mode(self, easy_clicked, medium_clicked, hard_clicked) -> None:
        ''' Switch difficulty button. Only one difficulty button can be clicked at a time. '''
        if easy_clicked is True and self.easy_clicked is True:
            self.easy_clicked = False
            self.settings.reset_difficulty()
        elif easy_clicked is True:
            self.settings.switch_difficulty(1)
            self.easy_clicked = True
            self.medium_clicked = self.hard_clicked = False

        if medium_clicked is True and self.medium_clicked is True:
            self.medium_clicked = False
            self.settings.reset_difficulty()
        elif medium_clicked is True:
            self.settings.switch_difficulty(2)
            self.medium_clicked = True
            self.easy_clicked = self.hard_clicked = False

        if hard_clicked is True and self.hard_clicked is True:
            self.hard_clicked = False
            self.settings.reset_difficulty()
        elif hard_clicked is True:
            self.settings.switch_difficulty(3)
            self.hard_clicked = True
            self.easy_clicked = self.medium_clicked = False
