import pygame
from constants import *
from abc import ABC, abstractmethod
from enum import Enum, auto

pygame.init()


class PieceColor(Enum):
    BLACK = "b"
    WHITE = "w"


class PieceType(Enum):
    PAWN = "p"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    QUEEN = "Q"
    KING = "K"


pieces_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN, PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]


class Piece:
    def __init__(self, piece_color: PieceColor, piece_type: PieceType, board_coor: tuple):
        self.piece_color = piece_color
        self.piece_type = piece_type
        self.x = board_coor[0]
        self.y = board_coor[1]
        self.image = IMAGES[self.piece_color.value + self.piece_type.value]

    def draw(self):
        WIN.blit(self.image, (self.x * CLENGTH, self.y * CLENGTH))

    def __repr__(self):
        return f"{self.piece_color} {self.piece_type}"


class Cell:
    def __init__(self, coor: tuple, piece=None):
        self.x = coor[0]
        self.y = coor[1]
        self.xcor1 = self.x * CLENGTH
        self.xcor2 = self.x * CLENGTH + CLENGTH
        self.ycor1 = self.y * CLENGTH
        self.ycor2 = self.y * CLENGTH + CLENGTH
        self.color = [LCOLOR, RCOLOR][(self.x + self.y) % 2]
        self.selected = False
        self.highlighted = False
        self.piece = piece

    def draw(self):
        color = self.color
        if self.highlighted:
            color = HCOLOR
        elif self.selected:
            color = SCOLOR
        pygame.draw.rect(WIN, color, [self.xcor1, self.ycor1, CLENGTH, CLENGTH])
        if self.piece is not None:
            self.piece.draw()


class Board:
    def __init__(self):
        self.cells = [
            [Cell((i, 0), Piece(PieceColor.BLACK, pieces_order[i], (i, 0))) for i in range(8)],  # Black pieces
            [Cell((i, 1), Piece(PieceColor.BLACK, PieceType.PAWN, (i, 1))) for i in range(8)],  # Black pawns
            [Cell((i, 2)) for i in range(8)],  # Empty
            [Cell((i, 3)) for i in range(8)],  # Empty
            [Cell((i, 4)) for i in range(8)],  # Empty
            [Cell((i, 5)) for i in range(8)],  # Empty
            [Cell((i, 6), Piece(PieceColor.WHITE, PieceType.PAWN, (i, 6))) for i in range(8)],  # White pawns
            [Cell((i, 7), Piece(PieceColor.WHITE, pieces_order[i], (i, 7))) for i in range(8)]   # White pieces
        ]
        self.selected_piece = None
        self.piece_selected = False
        self.selected_cell = None

    # draw the board
    def draw(self):
        # draw each cell
        for row in self.cells:
            for cell in row:
                cell.draw()

    # function for when board has been clicked
    def clicked(self, pos: tuple):
        pass

    def highlight_cells(self, piece):
        pass

    def unselect_all_cells(self):
        for row in self.cells:
            for cell in row:
                cell.selected = False

