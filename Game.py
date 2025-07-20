import socket
import threading
import pygame
import json

from Piece import Piece

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess Game")

# Création du plateau d'échecs
board = [[None for _ in range(8)] for _ in range(8)]

def init_back_row(color, row):
    order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
    for col in range(8):
        board[row][col] = Piece(type=order[col], color=color)

def init_pawns(color, row):
    for col in range(8):
        board[row][col] = Piece(type="pawn", color=color)

init_back_row("black", 0)
init_pawns("black", 1)
init_pawns("white", 6)
init_back_row("white", 7)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Boucle de jeu
    screen.fill((255, 255, 255))
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                pygame.draw.rect(screen, (0, 0, 0), (col * 100, row * 100, 100, 100))
                pygame.draw.circle(screen, (255, 0, 0) if piece.color == 'white' else (0, 0, 255), 
                                   (col * 100 + 50, row * 100 + 50), 30)
    # Affichage des pièces sur le plateau
    pygame.display.flip()

pygame.quit()