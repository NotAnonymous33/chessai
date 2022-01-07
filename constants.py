import pygame
pygame.init()

STRING = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# STRING = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
DEPTH = 3  # speed = 0.02 * 24^(depth - 1)
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
_PNAMES = ["b", "k", "n", "p", "q", "r"]
IMAGES = {i: pygame.transform.scale(pygame.image.load("images/black/" + i + ".png"), (CLENGTH, CLENGTH)) for i in _PNAMES}
IMAGES.update({i.upper(): pygame.transform.scale(pygame.image.load("images/white/" + i.upper() + ".png"), (CLENGTH, CLENGTH)) for i in _PNAMES})
ba = ["rook", "knight", "bishop", "queen"]
NIMAGES = {i: pygame.transform.scale(pygame.image.load("images/" + i + ".png"), (CLENGTH, CLENGTH)) for i in ba}
WIN = pygame.display.set_mode((TLENGTH, TLENGTH + CLENGTH))

