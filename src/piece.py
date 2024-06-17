import os
import math


class Piece:
    def __init__(self, name, color, value, texture=None, texture_rec=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == "white" else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.set_texture()
        self.texture_rec = texture_rec

    def set_texture(self, size=80):
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.dirname(current_directory)

        self.texture = os.path.join(
            f"{parent_directory}/assets/images-{size}px/{self.color}_{self.name}.png"
        )

    def add_moves(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == "white" else 1
        self.en_passant = False
        super().__init__(name="pawn", color=color, value=1.0)


class Knight(Piece):
    def __init__(self, color):
        super().__init__(name="knight", color=color, value=3.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(name="bishop", color=color, value=3.0)


class Rook(Piece):
    def __init__(self, color):
        super().__init__(name="rook", color=color, value=5.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__(name="queen", color=color, value=9.0)


class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__(name="king", color=color, value=100000.0)
