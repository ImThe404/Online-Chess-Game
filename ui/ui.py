import pygame

class UI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

    def draw(self):
        self.screen.fill((255, 255, 255))
        for y in range(8):
            for x in range(8):
                rect = pygame.Rect(x * 64, y * 64, 64, 64)
                if self.game.selected_pos == (x, y):
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                elif (x, y) in self.game.legal_moves:
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)
                elif (x + y) % 2 == 0:
                    pygame.draw.rect(self.screen, (240, 217, 181), rect)
                else:
                    pygame.draw.rect(self.screen, (181, 136, 99), rect)

                piece = self.game.board.grid[y][x]
                if piece:
                    image = piece.get_image()
                    if image:
                        image = pygame.transform.scale(image, (64, 64))
                        self.screen.blit(image, rect.topleft)

    def handle_click(self, pos):
        x, y = pos[0] // 64, pos[1] // 64
        if not self.game.selected_piece:
            self.game.select_piece((x, y))
        else:
            moved = self.game.move_selected_piece((x, y))
            if not moved:
                self.game.select_piece((x, y))
