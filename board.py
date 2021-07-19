import pygame
from constants import *

pygame.init()


class Cell:
    def __init__(self, window, coor):
        self.x = coor[0]
        self.y = coor[1]
        self.color = [RCOLOR, LCOLOR][(self.x + self.y) % 2]
        self.window = window

    def draw(self):
        pygame.draw.rect(self.window, self.color, [self.x * WIDTH, self.y * WIDTH, WIDTH, WIDTH])


class Board:
    def __init__(self, window):
        self.cells = [[Cell(window, (i, j)) for j in range(8)] for i in range(8)]
        self.window = window

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw()
