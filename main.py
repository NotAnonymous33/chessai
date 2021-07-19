import pygame
from board import Board
from constants import *

pygame.init()

WIN = pygame.display.set_mode((LENGTH, LENGTH))

board = Board(WIN)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    board.draw()
pygame.quit()





