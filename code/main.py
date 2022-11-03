"""
Main module with instance of the game.
"""

from alien_invasion import AlienInvasion

if __name__ == "__main__":
    ai: AlienInvasion = AlienInvasion()
    ai.run_game()
