from core.board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "white"
        self.selected_piece = None
        self.selected_pos = None
        self.legal_moves = []

    def select_piece(self, pos):
        x, y = pos
        piece = self.board.get_piece(pos)
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            self.selected_pos = pos
            self.legal_moves = piece.get_legal_moves(pos, self.board.grid)
        else:
            self.clear_selection()

    def move_selected_piece(self, to_pos):
        if self.selected_piece and to_pos in self.legal_moves:
            self.board.move_piece(self.selected_pos, to_pos)
            self.turn = "black" if self.turn == "white" else "white"
            self.clear_selection()
            return True
        return False

    def clear_selection(self):
        self.selected_piece = None
        self.selected_pos = None
        self.legal_moves = []
