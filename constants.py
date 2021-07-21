import pygame
pygame.init()

LCOLOR = (240, 230, 220)
RCOLOR = (199, 117, 61)
SCOLOR = (0, 255, 255)
HCOLOR = (0, 181, 98)  # (127, 255, 0)
TLENGTH = 600
CLENGTH = TLENGTH // 8
FPS = 60
_PNAMES = ["bB", "bK", "bN", "bp", "bQ", "bR", "wB", "wK", "wN", "wp", "wQ", "wR"]
IMAGES = {i: pygame.transform.scale(pygame.image.load("images/" + i + ".png"), (CLENGTH, CLENGTH)) for i in _PNAMES}
WIN = pygame.display.set_mode((TLENGTH, TLENGTH + 50))

