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

class Piece:
    def __init__(self, window, piece_color: PieceColor, piece_type: PieceType, coor: tuple):
        self.window = window
        self.piece_color = piece_color
        self.piece_type = piece_type
        self.xcoor = coor[0]
        self.ycoor = coor[1]
        self.image = IMAGES[self.piece_color.value + self.piece_type.value]



    def draw(self):
        self.window.blit(self.image, (self.xcoor * CLENGTH, self.ycoor * CLENGTH))



class Cell:
    def __init__(self, window: pygame.display, coor: tuple):
        self.x = coor[0]
        self.y = coor[1]
        self.xcor1 = self.x * CLENGTH
        self.xcor2 = self.x * CLENGTH + CLENGTH
        self.ycor1 = self.y * CLENGTH
        self.ycor2 = self.y * CLENGTH + CLENGTH
        self.color = [LCOLOR, RCOLOR][(self.x + self.y) % 2]
        self.window = window
        self.selected = False
        self.piece = None

    def draw(self):
        pygame.draw.rect(self.window, [self.color, SCOLOR][self.selected], [self.x * CLENGTH, self.y * CLENGTH, CLENGTH, CLENGTH])


class Board:
    def __init__(self, window: pygame.display):
        self.cells = [[Cell(window, (i, j)) for j in range(8)] for i in range(8)]
        self.window = window
        self.pieces = [
            [],
            [Piece(self.window, PieceColor.BLACK, PieceType.PAWN, (i, 1)) for i in range(8)],
            [],
            [],
            [],
            [],
            [Piece(self.window, PieceColor.WHITE, PieceType.PAWN, (i, 6)) for i in range(8)],
            []
        ]

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw()
        for row in self.pieces:
            for piece in row:
                piece.draw()


    def set_selected(self, pos: tuple):
        for row in self.cells:
            for cell in row:
                if cell.xcor1 < pos[0] < cell.xcor2 and cell.ycor1 < pos[1] < cell.ycor2:
                    cell.selected = not cell.selected
                else:
                    cell.selected = False

