import pygame
from board import Board
from constants import *

pygame.init()



clock = pygame.time.Clock()

board = Board()

running = True

pygame.display.set_caption("Chess by Ismail Choudhury")



while running:
    pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

    if pos is not None:
        board.set_selected(pos)




    board.draw()
    pygame.display.flip()


    clock.tick(FPS)

pygame.quit()





