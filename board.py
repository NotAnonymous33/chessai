import pygame
from constants import *

pygame.init()


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

    def draw(self):
        pygame.draw.rect(self.window, [self.color, SCOLOR][self.selected], [self.x * CLENGTH, self.y * CLENGTH, CLENGTH, CLENGTH])


class Board:
    def __init__(self, window: pygame.display):
        self.extra = Cell(window, (9, 9))
        self.cells = [[Cell(window, (i, j)) for j in range(8)] for i in range(8)]
        self.window = window
        self.current_selected = self.extra

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw()

    def set_selected(self, pos: tuple):
        for row in self.cells:
            for cell in row:
                if cell.xcor1 < pos[0] < cell.xcor2 and cell.ycor1 < pos[1] < cell.ycor2:
                    if self.current_selected == cell:
                        cell.selected = False
                    else:
                        self.current_selected.selected = False
                        cell.selected = True
                        self.current_selected = cell
