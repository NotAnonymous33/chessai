from pieces import Cell
from constants import *

cells = [[Cell(col, row) for col in range(NUM_ROWS)] for row in range(NUM_ROWS)]


class Drawer:
    def __init__(self, win, data, font, pygame, images):
        self.win = win
        self.pygame = pygame
        self.font = font
        self.images = images

    def draw_piece(self, piece, x, y):
        if not piece.color.value:
            return
        img = self.images[piece.image]

        self.win.blit(img, (x * CLENGTH, y * CLENGTH))

    def draw_cells(self):
        for row in cells:
            for cell in row:
                self.pygame.draw.rect(self.win, cell.color, [cell.xcoor, cell.ycoor, CLENGTH, CLENGTH])

    def draw_highlighted(self, board):
        for coord in board.highlighted_cells:
            color = HLCOLOR
            if (coord[0] + coord[1]) % 2:
                color = HDCOLOR
            self.pygame.draw.rect(self.win, color, [coord[0] * CLENGTH, coord[1] * CLENGTH, CLENGTH, CLENGTH])

    def draw_pieces(self, board):
        for row_num in range(NUM_ROWS):
            for col_num in range(NUM_ROWS):
                self.draw_piece(board.pieces[row_num][col_num], col_num, row_num)

    def draw_promoting(self):
        for i, p in enumerate(["rook", "knight", "bishop", "queen"]):
            self.win.blit(NIMAGES[p], (i * CLENGTH, NUM_ROWS * CLENGTH))

    def draw(self, board):
        # draw the squares of the board
        self.win.fill((0, 0, 0))

        self.draw_cells()

        if board.promote:
            for i in range(4):
                cell = Cell(i, 8)
                self.pygame.draw.rect(self.win, cell.color, [cell.xcoor, cell.ycoor, CLENGTH, CLENGTH])

        # draw moved to square
        self.pygame.draw.rect(self.win, MTCOLOR,
                         [board.moved_to[0] * CLENGTH, board.moved_to[1] * CLENGTH, CLENGTH, CLENGTH])

        # draw highlighted squares
        self.draw_highlighted(board)

        # draw selected square
        self.pygame.draw.rect(self.win, SCOLOR,
                         [board.source_coord[0] * CLENGTH, board.source_coord[1] * CLENGTH, CLENGTH, CLENGTH])

        # draw pieces
        self.draw_pieces(board)

        if board.promote:
            self.draw_promoting()

    def draw_button(self, button):
        self.pygame.draw.rect(self.win, button.color, [button.x, button.y, button.width, button.height])
        self.win.blit(self.font.render(button.text, True, (0, 0, 0)), (button.x + 5, button.y))
