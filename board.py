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

    def __repr__(self):
        return f"({self.piece}) at ({self.x}, {self.y})"

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
        self.cell_selected = False

    # draw the board
    def draw(self):
        # draw each cell
        for row in self.cells:
            for cell in row:
                cell.draw()

    # function for when board has been clicked
    def clicked(self, pos: tuple):
        if not (0 < pos[0] < TLENGTH and 0 < pos[1] < TLENGTH):
            self.reset_selected()
        else:
            x = pos[0] // CLENGTH
            y = pos[1] // CLENGTH
            if self.cell_selected:
                self.selected_cell.selected = False
            else:
                self.selected_cell = self.cells[y][x]
                self.selected_cell.selected = True
            self.cell_selected = not self.cell_selected


        print(self.selected_piece)



        """
        // If the click is outside the range of the board, set everything to default values
        Otherwise:
            Things that happen when there is a click on a cell
            
            //If there is a selected cell
            //    do some stuff
            //if there is not a selected cell
            //    Set the clicked cell to the selected cell
            
            //If the cell is selected, set this cell to off
            //If the cell is not selected, set the selected cell to off and select this cell
            
            
            If there is a selected piece
                Move to the cell to the new cell
            
            If there is not a selected piece
                If there is a piece in the cell, set the piece as the current piece
                If there is not a piece in the cell, set the current piece to None
    

        """

        pass

    def reset_selected(self):
        self.selected_piece = None
        self.piece_selected = False
        self.selected_cell = None

    def highlight_cells(self, piece):
        pass

    def unselect_all_cells(self):
        for row in self.cells:
            for cell in row:
                cell.selected = False

