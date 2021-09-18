import random

import pygame

import json

import sys
from settings import Settings
from bird import Bird
from pipe import PipeUp, PipeDown
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


class FlappyBird:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize pygame and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Flappy Bird")

        # Create an instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.bird = Bird(self)
        self.pipes = pygame.sprite.Group()

        # Create an identical group of pipes to aid scoring. We will remove the pipes from this group as soon as
        # the bird passes through and let the others from the other group continue until the end of the screen.
        self.copy_of_row_of_pipes = pygame.sprite.Group()

        self._create_pipe_rows()

        # Make the play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""

        while True:
            self._check_events()

            if self.stats.game_active:
                self.bird.update()
                self._update_pipes()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('high_score.txt', 'w') as hs:
                    json.dump(self.stats.high_score, hs)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""

        if event.key == pygame.K_SPACE:
            self.bird.jumping = True
        elif event.key == pygame.K_q:
            with open('high_score.txt', 'w') as hs:
                json.dump(self.stats.high_score, hs)
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""

        if event.key == pygame.K_SPACE:
            self.bird.jumping = False

    def _create_pipe_rows(self):
        """Create the pipes moving across the screen."""
        # Make 25 pipes in each row.
        # Spacing between each pipe is equal to two pipe widths.

        if len(self.copy_of_row_of_pipes) < 3:
            for pipe_number in range(25):
                self._create_pipe(pipe_number)

    def _create_pipe(self, pipe_number):

        pipe_width = float(self.settings.pipe_gap)

        # Create a downward facing pipe and place it in the row.
        pipe_down = PipeDown(self)
        pipe_down.x = pipe_down.rect.x + 2 * pipe_width * pipe_number
        pipe_down.rect.x = pipe_down.x
        pipe_down.rect.y = random.randint(-470, -60)
        self.pipes.add(pipe_down)

        # Create an identical row of downward facing pipes for scoring purposes.
        self.copy_of_row_of_pipes.add(pipe_down)

        # Create upward facing pipe and place it in the row.
        pipe_up = PipeUp(self)
        pipe_up.x = pipe_up.rect.x + 2 * pipe_width * pipe_number
        pipe_up.rect.x = pipe_up.x
        pipe_up.rect.y = (pipe_down.rect.y + 600) + (float(self.bird.new_rect.height) * 2)
        self.pipes.add(pipe_up)

        # Create an identical row of upward facing pipes for scoring purposes.
        self.copy_of_row_of_pipes.add(pipe_up)

    def _update_pipes(self):
        """Update the positions of all pipes in both pipe rows and get rid of old pipes."""

        self.pipes.update()
        self._create_pipe_rows()

        # Look for bird-pipe collisions.
        if pygame.sprite.spritecollideany(self.bird, self.pipes):
            self._pipe_hit()

        # Look for the bird hitting the bottom.
        self._check_bird_bottom()

        # Check whether the bird has passed through a pipe and implement scoring and speed.
        self._check_bird_through()

        # Remove pipes that moved out of screen.
        self._check_pipe_out_of_screen()

    def _check_bird_through(self):
        """Check if the bird has successfully made it through the pipes and increase difficulty if so."""

        for pipe in self.copy_of_row_of_pipes.copy():
            if self.bird.rect.left >= pipe.rect.centerx:
                self.copy_of_row_of_pipes.remove(pipe)
                pygame.mixer.Sound.play(self.settings.bird_sound)
                self.settings.increase_speed()
                self.stats.score += 1 / 2
                self.sb.prep_score()
                self.sb.check_high_score()

    def _check_pipe_out_of_screen(self):
        """Check for and remove pipes that left the screen."""

        for pipe in self.pipes.copy():
            if pipe.rect.right <= 0:
                self.pipes.remove(pipe)

    def _pipe_hit(self):
        """Respond to pipe being hit by the bird."""

        # Play game-over sound.
        pygame.mixer.Sound.play(self.settings.game_over_sound)

        # Get rid of remaining pipes.
        self.pipes.empty()
        self.copy_of_row_of_pipes.empty()

        # Create new rows of pipes and put the bird in its starting position.
        self._create_pipe_rows()
        self.bird.start_bird()

        # End the game.
        self.stats.game_active = False
        pygame.mouse.set_visible(True)

    def _check_bird_bottom(self):
        """Check if the bird has hit the bottom."""

        screen_rect = self.screen.get_rect()
        if self.bird.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if a pipe got hit.
            self._pipe_hit()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        self.screen.fill(self.settings.bg_colour)
        self.bird.blitme()
        self.pipes.draw(self.screen)
        self.copy_of_row_of_pipes.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make game instance and run game.
    fb = FlappyBird()
    fb.run_game()
