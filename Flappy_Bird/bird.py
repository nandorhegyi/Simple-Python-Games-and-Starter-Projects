import pygame


class Bird:
    """A class to manage the bird."""

    def __init__(self, fb_game):
        """Initialize the bird and set its starting position."""

        self.screen = fb_game.screen
        self.settings = fb_game.settings
        self.screen_rect = fb_game.screen.get_rect()

        # Load the bird image and get its rect.
        self.image = pygame.image.load('images/bird.bmp')
        self.rect = self.image.get_rect()

        # Attributes of the rotated image.
        self.rotated_image, self.new_rect = self._rot_bird_image(45)

        # Set the bird pictures slightly left of the centre of the screen.
        self.rect.midright = self.screen_rect.center
        self.new_rect.midright = self.screen_rect.center

        # Store a decimal value for the bird's vertical position.
        self.y = float(self.rect.y)

        # Movement flag.
        self.jumping = False

    def _rot_bird_image(self, angle):
        """Rotate the bird image to illustrate falling."""

        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)

        return rotated_image, new_rect

    def update(self):
        """Update the bird's position based on the movement flag."""

        # Update the bird's y value not the rect.
        if self.jumping:
            self.y -= self.settings.jumping_speed
        # If falling.
        self.y += self.settings.falling_speed

        # Update rect objects from self.y.
        self.rect.y = self.y
        self.new_rect.y = self.y

    def blitme(self):
        """Draw the bird at its current location."""

        # At the start or when bird is flying/jumping.
        if self.jumping:
            self.screen.blit(self.rotated_image, self.new_rect)
        else:
            self.screen.blit(self.image, self.rect)

    def start_bird(self):
        """Put the bird back to its starting position."""

        self.rect.midright = self.screen_rect.center
        self.new_rect.midright = self.screen_rect.center
        self.y = float(self.rect.y)


