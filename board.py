# import pygame
from constants import *
from aenum import Enum as AEnum
from aenum import NoAlias
from enum import Enum

pygame.init()


class PieceColor(Enum):
    BLACK = -1
    WHITE = 1
    EMPTY = 0


class PieceType(AEnum):
    _settings_ = NoAlias
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
        self.moved = False

    def draw(self, x, y):
        WIN.blit(self.image, (x * CLENGTH, y * CLENGTH))

    def __repr__(self):
        return f"{self.color} {self.piece_type}"


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

    def __repr__(self):
        return "empty"

    def draw(self, *args, **kwargs):
        pass


class Board:
    def __init__(self):
        self.cells = [[Cell(col, row) for col in range(NUM_ROWS)] for row in range(NUM_ROWS)]
        self.pieces = [
            [Piece(i, 0) for i in range(NUM_ROWS)],
            [Piece(i, 1) for i in range(NUM_ROWS)],
            [Empty() for _ in range(NUM_ROWS)],
            [Empty() for _ in range(NUM_ROWS)],
            [Empty() for _ in range(NUM_ROWS)],
            [Empty() for _ in range(NUM_ROWS)],
            [Piece(i, 6) for i in range(NUM_ROWS)],
            [Piece(i, 7) for i in range(NUM_ROWS)]
        ]
        self.source_coord = (-1, -1)
        self.turn = 1
        self.highlighted_cells = set([])

    def draw(self):
        # draw the squares of the board
        for row in self.cells:
            for cell in row:
                cell.draw()

        # draw highlighted squares
        for coord in self.highlighted_cells:
            pygame.draw.rect(WIN, HCOLOR, [coord[0] * CLENGTH, coord[1] * CLENGTH, CLENGTH, CLENGTH])

        # draw selected square
        pygame.draw.rect(WIN, SCOLOR, [self.source_coord[0] * CLENGTH, self.source_coord[1] * CLENGTH, CLENGTH, CLENGTH])

        # draw pieces
        for row_num in range(NUM_ROWS):
            for col_num in range(NUM_ROWS):
                self.pieces[row_num][col_num].draw(col_num, row_num)

    def click(self, xpos, ypos):
        xc = xpos // CLENGTH
        yc = ypos // CLENGTH

        # if the click is outside the board, reset the pieces
        if not (0 <= xc <= 7 and 0 <= yc <= 7):  # de morgans law moment
            self.reset_source()
            return

        # if there isn't a source cell
        if self.source_coord == (-1, -1):
            if self.pieces[yc][xc].color.value == self.turn:  # if a cell with a piece is clicked
                self.source_coord = (xc, yc)  # set the clicked piece as the source piece
                self.highlight_cells()
            else:
                self.reset_source()
            return

        # there is a source cell
        if (xc, yc) in self.highlighted_cells:
            self.move_piece(xc, yc)
        self.reset_source()

    def highlight_cells(self):
        x, y = self.source_coord  # really do be wishing python 3.10 were here
        if self.pieces[y][x].piece_type == PieceType.PAWN:
            self.highlight_pawn()
        elif self.pieces[y][x].piece_type == PieceType.BISHOP:
            self.highlight_bishop()
        elif self.pieces[y][x].piece_type == PieceType.KNIGHT:
            self.highlight_knight()
        elif self.pieces[y][x].piece_type == PieceType.ROOK:
            self.highlight_rook()
        elif self.pieces[y][x].piece_type == PieceType.QUEEN:
            self.highlight_queen()
        elif self.pieces[y][x].piece_type == PieceType.KING:
            self.highlight_king()

    def highlight_pawn(self):
        x, y = self.source_coord
        # if the piece in front is empty add that cell
        if self.pieces[y - self.turn][x].color.value == 0:
            self.highlighted_cells.add((x, y - self.turn))

        # if the pawn hasn't moved, let it move 2 moves forward
        if not self.pieces[y][x].moved and self.pieces[y - 2 * self.turn][x].color.value == self.pieces[y - self.turn][x].color.value == 0:
            self.highlighted_cells.add((x, y - 2 * self.turn))

        # if the piece to the left and right corner are opposite color, add them to highlighted piece
        # left hand side
        if x != 0:
            if self.pieces[y - self.turn][x - 1].color.value == self.turn * -1:
                self.highlighted_cells.add((x - 1, y - self.turn))

        # right hand side
        if x != 7:
            if self.pieces[y - self.turn][x + 1].color.value == self.turn * -1:
                self.highlighted_cells.add((x + 1, y - self.turn))

    def highlight_bishop(self):
        pass

    def highlight_knight(self):
        # 2 right 1 up
        self.check_knight(2, -1)
        # 2 right 1 down
        self.check_knight(2, 1)
        # 1 right 2 up
        self.check_knight(1, -2)
        # 1 right 2 down
        self.check_knight(1, 2)
        # 2 left 1 up
        self.check_knight(-2, -1)
        # 2 left 1 down
        self.check_knight(-2, 1)
        # 1 left 2 up
        self.check_knight(-1, -2)
        # 1 left 2 down
        self.check_knight(-1, 2)

    def check_knight(self, dx, dy):
        x, y = self.source_coord
        if not (0 <= x + dx <= 7): return
        if not (0 <= y + dy <= 7): return
        if self.pieces[y + dy][x + dx].color.value != self.turn:  # 2 right 1 up
            self.highlighted_cells.add((x + dx, y + dy))

    def highlight_queen(self):
        self.highlight_rook()

    def highlight_rook(self):
        x, y = self.source_coord
        right = left = up = down = True

        difference = 1
        while right:
            if difference + x <= 7:
                if self.pieces[y][x + difference].color.value == self.turn * -1:
                    self.highlighted_cells.add((x + difference, y))
                    right = False
                elif self.pieces[y][x + difference].color.value == self.turn:
                    right = False
                else:
                    self.highlighted_cells.add((x + difference, y))
                difference += 1
            else:
                right = False

        # look left
        difference = -1
        while left:
            if difference + x >= 0:
                if self.pieces[y][x + difference].color.value == self.turn * -1:
                    self.highlighted_cells.add((x + difference, y))
                    left = False
                elif self.pieces[y][x + difference].color.value == self.turn:
                    left = False
                else:
                    self.highlighted_cells.add((x + difference, y))
                difference -= 1
            else:
                left = False

        # look up
        difference = -1
        while up:
            if difference + y >= 0:
                if self.pieces[y + difference][x].color.value == self.turn * -1:
                    self.highlighted_cells.add((x, y + difference))
                    up = False
                elif self.pieces[y + difference][x].color.value == self.turn:
                    up = False
                else:
                    self.highlighted_cells.add((x, y + difference))
                difference -= 1
            else:
                up = False

        difference = 1
        # look down
        while down:
            if difference + y <= 7:
                if self.pieces[y + difference][x].color.value == self.turn * -1:
                    self.highlighted_cells.add((x, y + difference))
                    down = False
                elif self.pieces[y + difference][x].color.value == self.turn:
                    down = False
                else:
                    self.highlighted_cells.add((x, y + difference))
                difference += 1
            else:
                down = False

    def highlight_king(self):
        # check up
        # check down
        # check left
        # check right
        # check up right
        # check up left
        # check down right
        # check down left
        pass

    def check_quit(self):
        return False

    def reset_source(self):
        self.source_coord = (-1, -1)
        self.highlighted_cells = set([])

    def move_piece(self, x, y):
        self.pieces[y][x] = self.pieces[self.source_coord[1]][self.source_coord[0]]
        self.pieces[y][x].moved = True
        self.pieces[self.source_coord[1]][self.source_coord[0]] = Empty()  # set the source piece to 0
        self.turn *= -1
