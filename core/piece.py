import pygame
import os

class Piece:
    def __init__(self, color):
        self.color = color    

    def __repr__(self):
        return f"{self.color[0].upper()}{self.type[0].upper()}"
    
    def get_legal_moves(self, pos, board):
        raise NotImplementedError
    
    def get_image(self):
        # Placeholder for image retrieval logic
        image_path = f"assets/{self.color}_{self.type}.png"
        if not os.path.exists(image_path):
            image_path = "assets/NoImage.png"
        try:
            return pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            return pygame.image.load("assets/NoImage.png").convert_alpha()
        
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "pawn"

    def get_legal_moves(self, pos, board):
        x, y = pos
        direction = -1 if self.color == "white" else 1
        moves = []

        # Avancer d'une case
        print("'''''")
        print("1:", y+ direction, "  2:", x)
        if board[y + direction][x] is None:
            moves.append((x, y + direction))

            # Première avancée de 2 cases
            start_row = 6 if self.color == "white" else 1
            if y == start_row and board[y + 2 * direction][x] is None:
                moves.append((x, y + 2 * direction))

        # Captures diagonales
        for dx in [-1, 1]:
            nx = x + dx
            ny = y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target and target.color != self.color:
                    moves.append((nx, ny))

        return moves
    
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "knight"

    def get_legal_moves(self, pos, board):
        x, y = pos
        moves = []
        directions = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target is None or target.color != self.color:
                    moves.append((nx, ny))
        return moves
    
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "rook"

    def get_legal_moves(self, pos, board):
        x, y = pos
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[ny][nx]
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "bishop"

    def get_legal_moves(self, pos, board):
        x, y = pos
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[ny][nx]
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "queen"

    def get_legal_moves(self, pos, board):
        # Combine les déplacements de la tour et du fou
        return Rook(self.color).get_legal_moves(pos, board) + \
               Bishop(self.color).get_legal_moves(pos, board)

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "king"
        
    def get_legal_moves(self, pos, board):
        x, y = pos
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[ny][nx]
                    if target is None or target.color != self.color:
                        moves.append((nx, ny))
        return moves
