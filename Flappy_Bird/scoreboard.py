import pygame.font


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, fb_game):
        """Initialize scorekeeping attributes."""

        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = fb_game.settings
        self.stats = fb_game.stats

        # Font settings for scoring information.
        self.text_colour = (240, 0, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """Turn the score into a rendered image."""

        score_str = str(round(self.stats.score))
        self.score_image = self.font.render(score_str, True, self.text_colour)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""

        high_score_str = ("High Score ") + str(round(self.stats.high_score))
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw score to the screen."""

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def check_high_score(self):
        """Check to see if there's a new high score."""

        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
