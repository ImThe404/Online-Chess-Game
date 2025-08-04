from core.game import Game
from ui.ui import UI
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    pygame.display.set_caption("Chess Game")

    game = Game(is_server=False, host='127.0.0.1', port=5000)
    ui = UI(screen, game)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ui.handle_click(pygame.mouse.get_pos())

        ui.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
