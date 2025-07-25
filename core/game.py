from core.board import Board
from net.network import NetworkClient, NetworkServer

class Game:
    def __init__(self, is_server=False, host='localhost', port=7777):
        self.board = Board()
        self.turn = "white"
        self.selected_piece = None
        self.selected_pos = None
        self.legal_moves = []

        self.network = None
        self.color = "white" if is_server else "black"

        if is_server:
            self.network = NetworkServer(host=host, port=port)
        else:
            self.network = NetworkClient(host=host, port=port)

        self.network.on_message = self.handle_remote_message

    def select_piece(self, pos):
        piece = self.board.get_piece(pos)
        if piece and piece.color == self.turn and piece.color == self.color:
            self.selected_piece = piece
            self.selected_pos = pos
            self.legal_moves = piece.get_legal_moves(pos, self.board.grid)
        else:
            self.clear_selection()

    def move_selected_piece(self, to_pos):
        if self.selected_piece and to_pos in self.legal_moves:
            self.board.move_piece(self.selected_pos, to_pos)
            self.turn = "black" if self.turn == "white" else "white"
            self.send_move(self.selected_pos, to_pos)
            self.clear_selection()
            return True
        return False

    def send_move(self, from_pos, to_pos):
        if self.network:
            self.network.send({
                "type": "move",
                "from": from_pos,
                "to": to_pos
            })

    def handle_remote_message(self, message):
        if message.get("type") == "move":
            from_pos = tuple(message["from"])
            to_pos = tuple(message["to"])
            self.board.move_piece(from_pos, to_pos)
            self.turn = "black" if self.turn == "white" else "white"
            self.clear_selection()

    def clear_selection(self):
        self.selected_piece = None
        self.selected_pos = None
        self.legal_moves = []
