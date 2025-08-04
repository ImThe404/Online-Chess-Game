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
            ##possible_moves = piece.get_legal_moves(pos, self.board.grid)
            ##legal_moves = []
            ##for move in possible_moves:
            ##    captured = self.board.grid[move[0]][move[1]]
            ##    self.board.grid[move[0]][move[1]] = piece
            ##    self.board.grid[pos[0]][pos[1]] = None
            ##    if not self.is_in_check(self.turn):
            ##        legal_moves.append(move)
            ##    self.board.grid[pos[0]][pos[1]] = piece
            ##    self.board.grid[move[0]][move[1]] = captured
            ##
            ##self.legal_moves = legal_moves
        else:
            self.clear_selection()

    def move_selected_piece(self, to_pos):
        if self.selected_piece and to_pos in self.legal_moves:
            self.board.move_piece(self.selected_pos, to_pos)
            self.turn = "black" if self.turn == "white" else "white"
            self.send_move(self.selected_pos, to_pos)
            self.clear_selection()
            ##if self.is_in_check(self.turn):
            ##    if not self.has_legal_moves(self.turn):
            ##        print(f"Échec et mat ! {self.turn} a perdu.")
            ##    else:
            ##        print(f"{self.turn} est en échec !")
            ##elif not self.has_legal_moves(self.turn):
            ##    print("Pat ! Match nul.")   
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

    def is_in_check(self, color):
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.type == "king" and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        if not king_pos:
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color != color:
                    print("row:", row, "col:", col, "piece:", piece)
                    moves = piece.get_legal_moves((row, col), self.board.grid)
                    if king_pos in moves:
                        return True

        return False
    
    def has_legal_moves(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == color:
                    from_pos = (row, col)
                    moves = piece.get_legal_moves(from_pos, self.board.grid)
                    for to_pos in moves:
                        captured = self.board.grid[to_pos[0]][to_pos[1]]
                        self.board.grid[to_pos[0]][to_pos[1]] = piece
                        self.board.grid[from_pos[0]][from_pos[1]] = None

                        in_check = self.is_in_check(color)

                        self.board.grid[from_pos[0]][from_pos[1]] = piece
                        self.board.grid[to_pos[0]][to_pos[1]] = captured

                        if not in_check:
                            return True 
        return False


