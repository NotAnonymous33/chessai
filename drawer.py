from pieces import Cell, Piece
from constants import *

cells = [[Cell(col, row) for col in range(NUM_ROWS)] for row in range(NUM_ROWS)]


def draw_piece(piece, x, y):
    if not piece.color.value:
        return
    if y == 8:
        img = NIMAGES[piece.image]
    else:
        img = IMAGES[piece.image]

    WIN.blit(img, (x * CLENGTH, y * CLENGTH))


def draw_cells():
    for row in cells:
        for cell in row:
            cell.draw()


def draw_highlighted(board):
    for coord in board.highlighted_cells:
        color = HLCOLOR
        if (coord[0] + coord[1]) % 2:
            color = HDCOLOR
        pygame.draw.rect(WIN, color, [coord[0] * CLENGTH, coord[1] * CLENGTH, CLENGTH, CLENGTH])


def draw_pieces(board):
    for row_num in range(NUM_ROWS):
        for col_num in range(NUM_ROWS):
            draw_piece(board.pieces[row_num][col_num], col_num, row_num)


def draw(board):
    # draw the squares of the board
    WIN.fill((0, 0, 0))

    draw_cells()

    if board.promote:
        for i in range(4):
            cell = Cell(i, 8)
            cell.draw()

    # draw moved to square
    pygame.draw.rect(WIN, (255, 0, 0),
                     [board.moved_to[0] * CLENGTH, board.moved_to[1] * CLENGTH, CLENGTH, CLENGTH])

    # draw highlighted squares
    draw_highlighted(board)

    # draw selected square
    pygame.draw.rect(WIN, SCOLOR,
                     [board.source_coord[0] * CLENGTH, board.source_coord[1] * CLENGTH, CLENGTH, CLENGTH])


    # draw pieces
    draw_pieces(board)

    if board.promote:
        for i in range(4):
            piece = Piece(i, 8)
            draw_piece(piece, i, 8)
