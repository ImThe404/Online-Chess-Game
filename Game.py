import socket
import threading
import pygame
import json

from Piece import *

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Chess Game")

# Création du plateau d'échecs
board = [[None for _ in range(8)] for _ in range(8)]

def init_back_row(color, row):
    order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for col in range(8):
        board[row][col] = order[col](color)

def init_pawns(color, row):
    for col in range(8):
        board[row][col] = Pawn(color)

# Initialisation du plateau
init_back_row("black", 0)
init_pawns("black", 1)
init_pawns("white", 6)
init_back_row("white", 7)


# Boucle principale
running = True
selected_piece = None
old_selected_row, old_selected_col = -1, -1
selected_row, selected_col = -1, -1
legal_moves = []
turn = "white"  # Initialiser le tour à "white"

def cancel_selection():
    global selected_piece, selected_row, selected_col, legal_moves
    selected_piece = None
    selected_row, selected_col = -1, -1
    legal_moves = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            old_selected_row, old_selected_col = selected_row, selected_col
            selected_col = mouse_x // 64
            selected_row = mouse_y // 64
            if 0 <= selected_row < 8 and 0 <= selected_col < 8:
                    if selected_piece and (selected_col, selected_row) in legal_moves:
                        # Déplacer la pièce
                        board[selected_row][selected_col] = selected_piece
                        board[old_selected_row][old_selected_col] = None
                        cancel_selection()
                        turn = "black" if turn == "white" else "white"  # Changer de tour
                    elif board[selected_row][selected_col] != None:
                        # Sélection d'une pièce
                        selected_piece = board[selected_row][selected_col]
                        if selected_piece.color != turn:
                            print(f"Cannot select {selected_piece.type} of color {selected_piece.color} on {turn}'s turn.")
                            cancel_selection()
                        else:
                            # Obtenir les mouvements légaux de la pièce sélectionnée
                            legal_moves = selected_piece.get_legal_moves((selected_col, selected_row), board)
                    else:
                        # Sélection dans une case vide
                        cancel_selection()
            if selected_piece:
                print(f"Piece selected at ({selected_row}, {selected_col}): {selected_piece.type} {selected_piece.color}")
                legal_moves = selected_piece.get_legal_moves((selected_col, selected_row), board)

    # Boucle de jeu
    screen.fill((255, 255, 255))
    for row in range(8):
        for col in range(8):
            if selected_col == col and selected_row == row:
                pygame.draw.rect(screen, (0, 200, 0), (col * 64, row * 64, 64, 64))
            elif (col, row) in legal_moves:
                pygame.draw.rect(screen, (0, 0, 200), (col * 64, row * 64, 64, 64))
            elif row % 2 == col % 2:
                pygame.draw.rect(screen, (200, 200, 200), (col * 64, row * 64, 64, 64))
            else:
                pygame.draw.rect(screen, (100, 100, 100), (col * 64, row * 64, 64, 64))
            piece = board[row][col]
            if piece:
                image = piece.get_image()
                if image:
                    image = pygame.transform.scale(image, (64, 64))
                    screen.blit(image, (col * 64, row * 64))
                else:
                    # Placeholder for drawing pieces if no image is available
                    pygame.draw.circle(screen, (255, 0, 0), (col * 64 + 50, row * 64 + 50), 30)

    # Affichage des pièces sur le plateau
    pygame.display.flip()

pygame.quit()