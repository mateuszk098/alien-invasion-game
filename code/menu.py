''' 
General file with menu management.
'''

from button import Button


class Menu():

    def __init__(self, ai_game) -> None:
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.play_button: Button = Button(ai_game, 'Play', -100)
        self.easy_mode_button: Button = Button(ai_game, 'Easy Mode', -25)
        self.medium_mode_button: Button = Button(ai_game, 'Medium Mode', 50)
        self.hard_mode_button: Button = Button(ai_game, 'Hard Mode', 125)

        self.easy_clicked: bool = False
        self.medium_clicked: bool = False
        self.hard_clicked: bool = False

    def draw_menu(self) -> None:
        self.play_button.draw_button()
        self.easy_mode_button.draw_button(self.easy_clicked)
        self.medium_mode_button.draw_button(self.medium_clicked)
        self.hard_mode_button.draw_button(self.hard_clicked)

    def check_play_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the play button is clicked by mouse. '''
        button_clicked: bool = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked is True:
            return True
        return False

    def check_difficulty_button(self, mouse_pos: tuple[int, int]) -> None:
        ''' Check if any difficulty button is clicked by mouse. '''
        easy_clicked: bool = self.easy_mode_button.rect.collidepoint(mouse_pos)
        medium_clicked: bool = self.medium_mode_button.rect.collidepoint(mouse_pos)
        hard_clicked: bool = self.hard_mode_button.rect.collidepoint(mouse_pos)
        self._switch_difficulty_mode(easy_clicked, medium_clicked, hard_clicked)

    def reset_buttons(self) -> None:
        ''' Reset difficulty buttons to default. '''
        self.easy_clicked = False
        self.medium_clicked = False
        self.hard_clicked = False

    def _switch_difficulty_mode(self, easy_clicked, medium_clicked, hard_clicked) -> None:
        ''' Switch difficulty button. Only one difficulty button can be clicked at a time. '''
        if easy_clicked is True and self.easy_clicked is True:
            self.easy_clicked = False
            self.settings.reset_difficulty()
            print('a')
        elif easy_clicked is True:
            self.settings.switch_difficulty(1)
            self.easy_clicked = True
            self.medium_clicked = self.hard_clicked = False
            print('b')

        if medium_clicked is True and self.medium_clicked is True:
            self.medium_clicked = False
            self.settings.reset_difficulty()
            print('c')
        elif medium_clicked is True:
            self.settings.switch_difficulty(2)
            self.medium_clicked = True
            self.easy_clicked = self.hard_clicked = False
            print('d')

        if hard_clicked is True and self.hard_clicked is True:
            self.hard_clicked = False
            self.settings.reset_difficulty()
            print('e')
        elif hard_clicked is True:
            self.settings.switch_difficulty(3)
            self.hard_clicked = True
            self.easy_clicked = self.medium_clicked = False
            print('f')
