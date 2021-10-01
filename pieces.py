from constants import *
from aenum import Enum, NoAlias

class PieceColor(Enum):
    Black = -1
    White = 1
    Empty = 0


class PieceType(Enum):
    # _settings_ = NoAlias
    Empty = 0
    Pawn = 100
    Rook = 500
    Bishop = 330
    Knight = 320
    Queen = 900
    King = 20000

pieces_order = [PieceType.Rook, PieceType.Knight, PieceType.Bishop, PieceType.Queen,
                PieceType.King, PieceType.Bishop, PieceType.Knight, PieceType.Rook]
pieces_order_char = ["R", "N", "B", "Q", "K", "B", "N", "R"]


class Piece:
    def __init__(self, x=-1, y=-1):
        # sorting out color of piece
        if x == -1:
            self.moved = False
            self.color = PieceColor.Empty
            self.piece_type = PieceType.Empty
            return
        if y < 3:
            self.color = PieceColor.Black
            img = "b"
        else:
            self.color = PieceColor.White
            img = "w"

        # type of piece
        if y == 0 or y == 7:
            self.piece_type = pieces_order[x]
            img += pieces_order_char[x]
        else:
            self.piece_type = PieceType.Pawn
            img += "p"

        # image of piece
        self.image = img
        if y == 8:
            self.image = ba[x]
        self.moved = False

    def __repr__(self):
        return f"{self.color} {self.piece_type}, {self.moved=}"

    def copyp(self):
        if not self.color.value:
            piece = Piece()
            return piece
        new = Piece(0, 0)
        new.color = self.color
        new.piece_type = self.piece_type
        new.moved = self.moved
        return new



class Cell:
    def __init__(self, x, y):
        self.xcoor = x * CLENGTH
        self.ycoor = y * CLENGTH
        self.color = [LCOLOR, RCOLOR][(x + y) % 2]

    def draw(self):
        pygame.draw.rect(WIN, self.color, [self.xcoor, self.ycoor, CLENGTH, CLENGTH])

    def __repr__(self):
        return f"({self.xcoor}, {self.ycoor})"

"""
class Empty:
    def __init__(self):
        self.color = PieceColor.Empty
        self.piece_type = PieceType.Empty

    def __repr__(self):
        return "empty"

    def draw(self, *args, **kwargs):
        pass

    def copyp(self):
        new = Empty()
        return new

"""