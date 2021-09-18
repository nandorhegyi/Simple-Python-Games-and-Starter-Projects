import json


class GameStats:
    """Track statistics for Flappy Bird."""

    def __init__(self, fb_game):
        """Initialize statistics."""

        self.settings = fb_game.settings
        self.reset_stats()

        # High score should never be reset and should be stored even if we exit the game.
        try:
            with open('high_score.txt') as hs:
                self.high_score = json.load(hs)
        except FileNotFoundError:
            self.high_score = 0

        # Start Flappy Bird in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""

        self.score = 0
