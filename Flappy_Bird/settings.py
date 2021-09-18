import pygame


class Settings:
    """A class to store all settings for the game."""

    def __init__(self):
        """Initialize the game's static settings."""

        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (255, 255, 255)

        # Pipe settings.
        self.pipe_gap = 250

        # Add sound effects.
        self.bird_sound = pygame.mixer.Sound('sound_effects/bird_noise.wav')
        self.game_over_sound = pygame.mixer.Sound('sound_effects/game_over.wav')

        # How quickly the game speeds up.
        self.speedup_scale = 1.01

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""

        # Bird setting.
        self.jumping_speed = 1.1
        self.falling_speed = 0.6

        # Pipe settings.
        self.pipe_speed = .4

    def increase_speed(self):
        """Increase speed settings."""

        self.jumping_speed *= self.speedup_scale
        self.falling_speed *= self.speedup_scale
        self.pipe_speed *= self.speedup_scale
