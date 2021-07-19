import pygame
from board import Board
from constants import *

pygame.init()


WIN = pygame.display.set_mode((TLENGTH, TLENGTH))
clock = pygame.time.Clock()

board = Board(WIN)

running = True

pygame.display.set_caption("Chess by Ismail Choudhury")



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    board.draw()

    pygame.display.flip()


    clock.tick(FPS)

pygame.quit()





