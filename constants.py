import pygame
pygame.init()

DEPTH = 3 # speed = 0.02 * 24^(depth - 1)
LCOLOR = (240, 230, 220)
RCOLOR = (199, 117, 61)
MCOLOR = (220, 173, 140)
SCOLOR = (0, 255, 255)
HDCOLOR = (0, 181, 98)  # (127, 255, 0)
HLCOLOR = (0, 255, 150)
TLENGTH = 600
CLENGTH = TLENGTH // 8
BCOLOR2 = (217, 128, 255)
BCOLOR = (179, 0, 255)
NUM_ROWS = 8
FPS = 60
_PNAMES = ["bB", "bK", "bN", "bp", "bQ", "bR", "wB", "wK", "wN", "wp", "wQ", "wR"]
IMAGES = {i: pygame.transform.scale(pygame.image.load("images/" + i + ".png"), (CLENGTH, CLENGTH)) for i in _PNAMES}
ba = ["R", "N", "B", "Q"]
NIMAGES = {i: pygame.transform.scale(pygame.image.load("images/" + i + ".png"), (CLENGTH, CLENGTH)) for i in ba}
WIN = pygame.display.set_mode((TLENGTH, TLENGTH + CLENGTH))

