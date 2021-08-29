from constants import *
from aenum import Enum, NoAlias

class PieceColor(Enum):
    BLACK = -1
    WHITE = 1
    EMPTY = 0


class PieceType(Enum):
    _settings_ = NoAlias
    EMPTY = 0
    PAWN = 1
    ROOK = 5
    BISHOP = 3
    KNIGHT = 3
    QUEEN = 9
    KING = 999999

pieces_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
                PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
pieces_order_char = ["R", "N", "B", "Q", "K", "B", "N", "R"]


class Piece:
    def __init__(self, x, y):
        # sorting out color of piece
        if y < 3:
            self.color = PieceColor.BLACK
            img = "b"
        else:
            self.color = PieceColor.WHITE
            img = "w"

        # type of piece
        if y == 0 or y == 7:
            self.piece_type = pieces_order[x]
            img += pieces_order_char[x]
        else:
            self.piece_type = PieceType.PAWN
            img += "p"

        # image of piece
        self.image = IMAGES[img]
        if y == 8:
            self.image = NIMAGES[ba[x]]
        self.moved = False

    def draw(self, x, y):
        WIN.blit(self.image, (x * CLENGTH, y * CLENGTH))

    def __repr__(self):
        return f"{self.color} {self.piece_type}, {self.moved=}"


class Cell:
    def __init__(self, x, y):
        self.xcoor = x * CLENGTH
        self.ycoor = y * CLENGTH
        self.color = [LCOLOR, RCOLOR][(x + y) % 2]

    def draw(self):
        pygame.draw.rect(WIN, self.color, [self.xcoor, self.ycoor, CLENGTH, CLENGTH])

    def __repr__(self):
        return f"({self.xcoor}, {self.ycoor})"


class Empty:
    def __init__(self):
        self.color = PieceColor.EMPTY
        self.piece_type = PieceType.EMPTY

    def __repr__(self):
        return "empty"

    def draw(self, *args, **kwargs):
        pass

