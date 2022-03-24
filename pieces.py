from constants import *
from enum import Enum


class PieceColor(Enum):
    Black = -1
    White = 1
    Empty = 0


class PieceType(Enum):
    Empty = 0
    Pawn = 100
    Rook = 500
    Bishop = 330
    Knight = 320
    Queen = 900
    King = 20000


pieces_dict = {"r": PieceType.Rook, "n": PieceType.Knight, "b": PieceType.Bishop, "q": PieceType.Queen,
               "k": PieceType.King, "p": PieceType.Pawn}


class Piece:
    def __init__(self, string="", moved=False, x=-1, y=-1, piece=None):
        if piece is not None:
            self.moved = piece.moved
            self.color = piece.color
            self.piece_type = piece.piece_type
            self.image = piece.image
            return

        # for blank pieces
        if string == "":
            self.moved = False
            self.color = PieceColor.Empty
            self.piece_type = PieceType.Empty
            self.image = ""
            return

        if string.isupper():
            self.color = PieceColor.White
        else:
            self.color = PieceColor.Black

        self.piece_type = pieces_dict[string.lower()]
        self.moved = moved
        self.image = string

        if self.piece_type == PieceType.Pawn:
            if self.color == PieceColor.White and y != 6 or self.color == PieceColor.Black and y != 1:
                self.moved = True

        elif self.piece_type == PieceType.King:
            if self.color == PieceColor.White:
                if x != 4 or y != 7:
                    self.moved = True
            elif self.color == PieceColor.Black:
                if x != 4 or y != 0:
                    self.moved = True

    def copy(self):
        new_piece = Piece(piece=self)
        return new_piece

    def __repr__(self):
        color = str(self.color).split(".")[1]
        type = str(self.piece_type).split(".")[1]
        return f"{color}{type}"


class Cell:
    def __init__(self, x, y, lcolor, rcolor):
        self.xcoor = x * CLENGTH
        self.ycoor = y * CLENGTH
        self.color = [lcolor, rcolor][(x + y) % 2]

    def __repr__(self):
        return f"({self.xcoor}, {self.ycoor})"
