from core.piece import Rook, Knight, Bishop, Queen, King, Pawn

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.init_board()

    def init_back_row(self, color, row):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.grid[row][col] = order[col](color)

    def init_pawns(self, color, row):
        for col in range(8):
            self.grid[row][col] = Pawn(color)

    def init_board(self):
        self.init_back_row("black", 0)
        self.init_pawns("black", 1)
        self.init_pawns("white", 6)
        self.init_back_row("white", 7)

    def move_piece(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos
        self.grid[ty][tx] = self.grid[fy][fx]
        self.grid[fy][fx] = None

    def get_piece(self, pos):
        x, y = pos
        return self.grid[y][x]
