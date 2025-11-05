import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, player, ai):
        # Move the ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

        # Check collision with paddles right after moving
        ball_rect = self.rect()

        if ball_rect.colliderect(player.rect()):
            self.x = player.rect().right  # Adjust position to avoid sticking
            self.velocity_x = abs(self.velocity_x)

        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.rect().left - self.width
            self.velocity_x = -abs(self.velocity_x)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
