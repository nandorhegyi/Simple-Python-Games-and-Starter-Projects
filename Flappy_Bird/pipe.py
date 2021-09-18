import pygame
from pygame.sprite import Sprite


class PipeDown(Sprite):
    """A class to represent the downward facing pipes from the game."""

    def __init__(self, fb_game):
        """Initialize the pipes and set their starting position."""

        super().__init__()
        self.screen = fb_game.screen
        self.settings = fb_game.settings

        self._make_downward_facing_pipe()

    def _make_downward_facing_pipe(self):

        # Load the downward pipe image and set its rect attributes.
        self.image = pygame.image.load('images/pipe_down.bmp')
        self.rect = self.image.get_rect()

        # Start the downward facing pipes on the right side of the screen.
        self.rect.x = self.screen.get_rect().width + 85

        # Store the downward facing pipes exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move downward facing pipe to the left."""

        self.x -= self.settings.pipe_speed
        self.rect.x = self.x


class PipeUp(Sprite):
    """A class to represent the upward facing pipes from the game."""

    def __init__(self, fb_game):
        """Initialize the pipes and set their starting position."""
        super().__init__()
        self.screen = fb_game.screen
        self.settings = fb_game.settings

        self._make_upward_facing_pipe()

    def _make_upward_facing_pipe(self):

        # Load the upward pipe image and set its rect attributes.
        self.image = pygame.image.load('images/pipe_up.bmp')
        self.rect = self.image.get_rect()

        # Start the upward facing pipe below the downward facing pipe.
        self.rect.x = self.screen.get_rect().width + 85

        # Store the upward facing pipe's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move upward facing pipe to the left."""

        self.x -= self.settings.pipe_speed
        self.rect.x = self.x




