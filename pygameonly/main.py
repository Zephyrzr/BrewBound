import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from game import GameManager

def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption(TITLE)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Inisialisasi Font Sistem dengan fallback
    try:
        font_large = pygame.font.SysFont("segoe ui emoji, segoe ui, dejavu sans, arial", 26, bold=True)
        font_regular = pygame.font.SysFont("segoe ui emoji, segoe ui, dejavu sans, arial", 18, bold=False)
        font_small = pygame.font.SysFont("segoe ui emoji, segoe ui, dejavu sans, arial", 14, bold=False)
    except Exception:
        font_large = pygame.font.Font(None, 32)
        font_regular = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 18)

    fonts = {
        "large": font_large,
        "regular": font_regular,
        "small": font_small
    }

    game = GameManager()

    running = True
    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        # Game Logic Update
        game.update()

        # Render Draw
        game.draw(screen, fonts)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
