
class Piece:
    def __init__(self, type, color):
        self.type = type      
        self.color = color    

    def __repr__(self):
        return f"{self.color[0].upper()}{self.type[0].upper()}"