import pygame
import numpy as np
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def generate_tone(freq=440, duration=0.1, volume=0.5):
    """Generate a short sine wave tone as a pygame Sound object."""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(freq * t * 2 * np.pi)
    audio = np.int16(tone * 32767 * volume)
    sound = pygame.mixer.Sound(buffer=audio)
    return sound


class GameEngine:
    def __init__(self, width, height, win_score=5):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.win_score = win_score

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 50)
        self.game_over = False
        self.winner_message = ""

        # 🎵 Generate in-memory sound effects
        self.sound_paddle = generate_tone(600, 0.05)
        self.sound_wall = generate_tone(400, 0.05)
        self.sound_score = generate_tone(250, 0.2)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        old_vel_x = self.ball.velocity_x
        old_vel_y = self.ball.velocity_y
        old_x = self.ball.x

        self.ball.move(self.player, self.ai)

        # Detect ball collisions via velocity change
        if self.ball.velocity_x != old_vel_x:
            self.sound_paddle.play()
        elif self.ball.velocity_y != old_vel_y:
            self.sound_wall.play()

        # Check if ball goes off-screen
        if self.ball.x <= 0:
            self.ai_score += 1
            self.sound_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.sound_score.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)
        self.check_game_over()

    def check_game_over(self):
        if self.player_score >= self.win_score:
            self.winner_message = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.win_score:
            self.winner_message = "AI Wins!"
            self.game_over = True

    def reset_game(self, new_win_score=None):
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner_message = ""
        if new_win_score:
            self.win_score = new_win_score
        self.ball.reset()

    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.game_over:
            text = self.game_over_font.render(self.winner_message, True, WHITE)
            rect = text.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text, rect)
