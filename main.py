import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60


def show_replay_menu(screen):
    """Display replay options and wait for user input."""
    font = pygame.font.SysFont("Arial", 40)
    options = [
        "Press 3 for Best of 3",
        "Press 5 for Best of 5",
        "Press 7 for Best of 7",
        "Press ESC to Exit"
    ]

    while True:
        screen.fill(BLACK)
        for i, text in enumerate(options):
            msg = font.render(text, True, WHITE)
            rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60 + i * 60))
            screen.blit(msg, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    return 3  # Best of 3 → win score 3
                elif event.key == pygame.K_5:
                    return 5  # Best of 5 → win score 5
                elif event.key == pygame.K_7:
                    return 7  # Best of 7 → win score 7
                elif event.key == pygame.K_ESCAPE:
                    return None
        clock.tick(30)


def main():
    running = True
    engine = GameEngine(WIDTH, HEIGHT)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

        # If game over, show replay menu
        if engine.game_over:
            pygame.time.wait(1500)  # small delay before showing menu
            new_win_score = show_replay_menu(SCREEN)
            if new_win_score:
                engine.reset_game(new_win_score)
            else:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()
