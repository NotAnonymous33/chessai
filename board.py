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
    def __init__(self, piece_color: PieceColor, piece_type: PieceType, coor: tuple):
        self.piece_color = piece_color
        self.piece_type = piece_type
        self.xcoor = coor[0]
        self.ycoor = coor[1]
        self.image = IMAGES[self.piece_color.value + self.piece_type.value]

    def draw(self):
        WIN.blit(self.image, (self.xcoor * CLENGTH, self.ycoor * CLENGTH))


class Cell:
    def __init__(self, coor: tuple):
        self.x = coor[0]
        self.y = coor[1]
        self.xcor1 = self.x * CLENGTH
        self.xcor2 = self.x * CLENGTH + CLENGTH
        self.ycor1 = self.y * CLENGTH
        self.ycor2 = self.y * CLENGTH + CLENGTH
        self.color = [LCOLOR, RCOLOR][(self.x + self.y) % 2]
        self.selected = False
        self.highlighted = False
        self.piece = None

    def draw(self):
        color = self.color
        if self.highlighted:
            color = HCOLOR
        elif self.selected:
            color = SCOLOR
        pygame.draw.rect(WIN, color, [self.xcor1, self.ycor1, CLENGTH, CLENGTH])


class Board:
    def __init__(self):
        self.cells = [[Cell((i, j)) for j in range(8)] for i in range(8)]
        self.pieces = [Piece(PieceColor.BLACK, pieces_order[i], (i, 0)) for i in range(8)] + \
                      [Piece(PieceColor.BLACK, PieceType.PAWN, (i, 1)) for i in range(8)] + \
                      [Piece(PieceColor.WHITE, PieceType.PAWN, (i, 6)) for i in range(8)] + \
                      [Piece(PieceColor.WHITE, pieces_order[i], (i, 7)) for i in range(8)]
        self.selected_piece = None
        self.piece_selected = False

    # draw the board
    def draw(self):
        # draw each cell
        for row in self.cells:
            for cell in row:
                cell.draw()
        # draw each piece
        for piece in self.pieces:
            piece.draw()

    # function for when board has been clicked
    def clicked(self, pos: tuple):
        # change the color of the cell which has been selected
        # set all other cells to default color
        for row in self.cells:
            for cell in row:
                if cell.xcor1 < pos[0] < cell.xcor2 and cell.ycor1 < pos[1] < cell.ycor2:
                    cell.selected = not cell.selected
                else:
                    cell.selected = False

        # if there is no current selected piece and a piece is clicked, set this as the current piece
        # if somewhere outside of board is clicked
        if (not 0 <= pos[0] // CLENGTH <= 7) or not(0 <= pos[1] // CLENGTH <= 7):
            for row in self.cells:
                for cell in row:
                    cell.selected = False
            self.piece_selected = False
        else:
            if not self.piece_selected:
                for piece in self.pieces:
                    if piece.xcoor == pos[0] // CLENGTH and piece.ycoor == pos[1] // CLENGTH:
                        if not self.piece_selected:
                            self.selected_piece = piece
                            print(self.selected_piece.piece_color, self.selected_piece.piece_type)
                            self.piece_selected = True
            # if there is a selected piece, change the position to the clicked position
            else:
                self.selected_piece.xcoor = pos[0] // CLENGTH
                self.selected_piece.ycoor = pos[1] // CLENGTH
                self.piece_selected = False
                self.cells[pos[0] // CLENGTH][pos[1] // CLENGTH].selected = False

    def highlight_cells(self, piece):
        pass

