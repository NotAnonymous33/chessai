from pieces import *
from copy import copy
import dis
from numpy import add

pawn_table = [[0, 0, 0, 0, 0, 0, 0, 0],
              [100, 100, 100, 100, 100, 100, 100, 100],
              [30, 30, 40, 60, 60, 40, 30, 30],
              [5, 5, 10, 25, 25, 10, 5, 5],
              [0, 0, 0, 20, 20, 0, 0, 0],
              [5, -5, -10, 0, 0, -10, -5, 5],
              [5, 10, 10, -20, -20, 10, 10, 5],
              [0, 0, 0, 0, 0, 0, 0, 0]]

knight_table = [[-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]]

bishop_table = [[-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20, ]]

rook_table = [[0, 0, 0, 0, 0, 0, 0, 0, ],
              [5, 10, 10, 10, 10, 10, 10, 5],
              [-5, 0, 0, 0, 0, 0, 0, -5],
              [-5, 0, 0, 0, 0, 0, 0, -5],
              [-5, 0, 0, 0, 0, 0, 0, -5],
              [-5, 0, 0, 0, 0, 0, 0, -5],
              [-5, 0, 0, 0, 0, 0, 0, -5],
              [0, 0, 0, 5, 5, 0, 0, 0]]

queen_table = [[-20, -10, -10, -5, -5, -10, -10, -20],
               [-10, 0, 0, 0, 0, 0, 0, -10],
               [-10, 0, 5, 5, 5, 5, 0, -10],
               [-5, 0, 5, 5, 5, 5, 0, -5],
               [0, 0, 5, 5, 5, 5, 0, -5],
               [-10, 5, 5, 5, 5, 5, 0, -10],
               [-10, 0, 5, 0, 0, 0, 0, -10],
               [-20, -10, -10, -5, -5, -10, -10, -20]]

empty_table = [[0 for i in range(8)] for j in range(8)]

tables = {
    PieceColor.White: {PieceType.Pawn: pawn_table, PieceType.Knight: knight_table, PieceType.Bishop: bishop_table,
                       PieceType.Rook: rook_table, PieceType.Queen: queen_table, PieceType.Empty: empty_table,
                       PieceType.King: empty_table},
    PieceColor.Black: {PieceType.Pawn: pawn_table[::-1], PieceType.Knight: knight_table,
                       PieceType.Bishop: bishop_table[::-1],
                       PieceType.Rook: rook_table[::-1], PieceType.Queen: [row[::-1] for row in queen_table[::-1]],
                       PieceType.Empty: empty_table,
                       PieceType.King: empty_table},
    PieceColor.Empty: {PieceType.Pawn: pawn_table, PieceType.Knight: knight_table, PieceType.Bishop: bishop_table,
                       PieceType.Rook: rook_table, PieceType.Queen: queen_table, PieceType.Empty: empty_table,
                       PieceType.King: empty_table}
}


def to_fen(board):
    string = ""
    count = 0
    for row in board.pieces:
        for piece in row:
            if piece.image == "":
                count += 1
            else:
                if count != 0:
                    string += str(count)
                    count = 0
                string += piece.image
        if count != 0:
            string += str(count)
            count = 0
        string += "/"
    string = string[:-1] + " "
    if board.turn == 1:
        string += "w"
    else:
        string += "b"

    return string


def fen_converter(string):
    pieces = []
    row = []
    row_num = 0
    col_num = 0
    for char in string:
        if char == "/":
            pieces.append(row)
            row = []
            row_num += 1
            col_num = 0
        elif char.isdigit():
            for _ in range(int(char)):
                row.append(Piece())
            col_num += int(char)

        else:
            row.append(Piece(char, x=col_num, y=row_num))
            col_num += 1

    pieces.append(row)
    return pieces


class Board:
    def __init__(self, depth=3, string=STRING):
        if depth == -1:
            self.white_king = self.black_king = self.turn = self.half = self.full = self.source_coord = self.moved_to \
                = self.highlighted_cells = self.check = self.quit = self.promote = self.ai = self.pieces = None
            return
        string = string.split()
        self.pieces = fen_converter(string[0])
        for y, row in enumerate(self.pieces):
            for x, piece in enumerate(row):
                if piece.piece_type is PieceType.King:
                    if piece.color is PieceColor.White:
                        self.white_king = (x, y)
                    else:
                        self.black_king = (x, y)

        # setting turns
        if len(string) == 1 or string[1] == "w":
            self.turn = 1
        else:
            self.turn = -1

        # setting clocks
        if len(string) == 1 or len(string) == 2:
            self.half = 0
            self.full = 0
        else:
            self.half = int(string[4])
            self.full = int(string[5])

            # setting castling
            if string[2] == "-":
                # no castling can happen
                self.move_kings([PieceColor.White, PieceColor.Black])
            else:
                # castling can happen
                if string[2].upper() == string[2]:  # lower case, white cannot castle
                    self.move_kings([PieceColor.White])
                elif string[2].lower() == string[2]:  # upper case, black cannot castle
                    self.move_kings([PieceColor.Black])

        self.source_coord = (-1, -1)
        self.moved_to = (-1, -1)
        self.highlighted_cells = set([])
        self.check = False
        self.quit = False
        self.promote = False
        self.ai = depth != 0

    def move_kings(self, colors):
        for row in self.pieces:
            for piece in row:
                if piece.piece_type == PieceType.King and piece.color in colors:
                    piece.moved = True

    def click(self, xpos, ypos):
        xc = xpos // CLENGTH
        yc = ypos // CLENGTH

        # if the click is outside the board, reset the pieces
        if not (0 <= xc <= 7 and 0 <= yc <= 7 + self.promote):  # de morgans law moment
            self.reset_source()
            return

        x, y = self.source_coord
        # if there isn't a source cell
        if self.source_coord == (-1, -1):
            if self.pieces[yc][xc].color.value is self.turn:  # if a cell with a piece is clicked
                self.source_coord = (xc, yc)  # set the clicked piece as the source piece
                self.highlight_cells(True)
                '''
                For each highlighted cell, make move
                If after move, still in check
                Remove move
                '''
            else:
                self.reset_source()
            return

        if y % 7 == 0 and self.pieces[y][x].piece_type == PieceType.Pawn:
            self.highlight_cells(True)
            if (xc, yc) not in self.highlighted_cells:
                return

            self.move_piece(xc, yc, True)

        if not self.promote and (xc, yc) in self.highlighted_cells:
            self.move_piece(xc, yc, True)

        with open("game.txt", "a") as file:
            file.write(to_fen(self) + "\n")
        with open("pgn.txt", "a") as file:
            if yc == 8:
                line = ""
            else:
                if self.turn == 1:
                    line = f"{self.pieces[yc][xc].image}{chr(xc + 97)}{8 - yc} "
                else:
                    line = f"{self.full}.{self.pieces[yc][xc].image}{chr(xc + 97)}{8 - yc} "
                    self.full += 1
            file.write(line)

        if not self.promote:
            self.reset_source()

    def highlight_cells(self, recur=False):
        x, y = self.source_coord
        if self.promote and self.pieces[y][x].piece_type is PieceType.Pawn and y % 7 == 0:
            self.highlighted_cells = set([(i, 8) for i in range(4)])
            return False
        self.highlighted_cells = set([])
        if self.pieces[y][x].piece_type is PieceType.Pawn:
            self.highlight_pawn()
        elif self.pieces[y][x].piece_type is PieceType.Bishop:
            self.highlight_bishop()
        elif self.pieces[y][x].piece_type is PieceType.Knight:
            self.highlight_knight()
        elif self.pieces[y][x].piece_type is PieceType.Rook:
            self.highlight_rook()
        elif self.pieces[y][x].piece_type is PieceType.Queen:
            self.highlight_queen()
        elif self.pieces[y][x].piece_type is PieceType.King:
            self.highlight_king()

        if recur:
            new_moves = set([])
            for move in self.highlighted_cells:
                new_board = self.copy_board()
                new_board.move_piece(*move)
                if not new_board.is_check():
                    new_moves.add(move)
            self.highlighted_cells = new_moves
        self.highlighted_cells.discard((x, y))


    def highlight_pawn(self):
        x, y = self.source_coord
        if y % 7 == 0:
            return
        # if the piece in front is empty add that cell
        if self.pieces[y - self.turn][x].color.value == 0:
            self.highlighted_cells.add((x, y - self.turn))

        # if the pawn hasn't moved, let it move 2 moves forward
        if not self.pieces[y][x].moved and \
                self.pieces[y - 2 * self.turn][x].color.value == self.pieces[y - self.turn][x].color.value == 0:
            self.highlighted_cells.add((x, y - 2 * self.turn))

        # if the piece to the left and right corner are opposite color, add them to highlighted piece
        # left hand side
        if x != 0:
            if self.pieces[y - self.turn][x - 1].color.value == self.turn * -1:
                self.highlighted_cells.add((x - 1, y - self.turn))

        # right hand side
        if x != 7:
            if self.pieces[y - self.turn][x + 1].color.value == self.turn * -1:
                self.highlighted_cells.add((x + 1, y - self.turn))

    def highlight_bishop(self):
        directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
        for direction in directions:
            self.check_direction(*direction)

    def highlight_knight(self):
        possible_moves = [(2, -1), (2, 1), (1, -2), (1, 2), (-2, -1), (-2, 1), (-1, -2), (-1, 2)]
        for move in possible_moves:
            self.check_cell(*move)

    def highlight_queen(self):
        self.highlight_rook()
        self.highlight_bishop()

    def highlight_rook(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction in directions:
            self.check_direction(*direction)

    def check_direction(self, d2x, d2y):
        dx = d2x
        dy = d2y
        x, y = self.source_coord
        while True:
            if not (0 <= x + dx <= 7 and 0 <= y + dy <= 7):
                return
            if self.pieces[y + dy][x + dx].color.value is self.turn * -1:
                self.highlighted_cells.add((x + dx, y + dy))
                return
            elif self.pieces[y + dy][x + dx].color.value is self.turn:
                return
            else:
                self.highlighted_cells.add((x + dx, y + dy))
                dx += d2x
                dy += d2y

    def highlight_king(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, -1), (-1, -1), (1, 1), (-1, 1)]
        for direction in directions:
            self.check_cell(*direction)

        x, y = self.source_coord
        # add castling to right
        if self.check:  # no castling allowed if in check
            return
        if self.pieces[y][x].moved:
            return  # no castling allowed if king has moved

        if not self.pieces[y][7].moved and \
                self.pieces[y][7].piece_type == PieceType.Rook and \
                self.pieces[y][7].color.value == self.turn and \
                (self.pieces[y][x + 1].color.value == self.pieces[y][x + 2].color.value == 0):
            self.highlighted_cells.add((x + 2, y))

        if not self.pieces[y][0].moved and \
                self.pieces[y][0].piece_type == PieceType.Rook and \
                self.pieces[y][0].color.value == self.turn and \
                (self.pieces[y][x - 1].color.value ==
                 self.pieces[y][x - 2].color.value ==
                 self.pieces[y][x - 3].color.value == 0):
            self.highlighted_cells.add((x - 2, y))
            self.highlighted_cells.add((x - 3, y))

    def check_cell(self, dx, dy):
        x, y = self.source_coord
        if not (0 <= y + dy <= 7 and 0 <= x + dx <= 7):
            return
        if self.pieces[y + dy][x + dx].color.value is not self.turn:
            self.highlighted_cells.add((x + dx, y + dy))

    def reset_source(self):
        self.source_coord = (-1, -1)
        self.highlighted_cells = set([])

    def move_piece(self, x, y, first=False):
        self.moved_to = (x, y)

        px, py = self.source_coord

        if self.pieces[py][px].piece_type == PieceType.Pawn and y % 7 == 0 and first:
            # wait for input from user asking which piece to turn into
            self.pieces[y][x] = self.pieces[py][px]
            self.pieces[py][px] = Piece()
            self.source_coord = (x, y)
            self.promote = True


            self.highlight_cells(True)
            return
            # get input
            # turn the piece into whatever type it should be

        if self.promote:
            if x == 0:
                promoting_piece = "R"
            elif x == 1:
                promoting_piece = "N"
            elif x == 2:
                promoting_piece = "B"
            elif x == 3:
                promoting_piece = "Q"
            if self.turn == -1:
                promoting_piece = promoting_piece.lower()
            self.pieces[py][px] = Piece(string=promoting_piece)
            self.pieces[py][px].moved = True
            self.promote = False

            current = self.source_coord
            self.check = self.is_check(None, (px, py))
            self.source_coord = current

        else:
            # castling
            if self.pieces[py][px].piece_type == PieceType.King:
                if self.turn == 1:
                    self.white_king = (x, y)
                else:
                    self.black_king = (x, y)
                if abs((d := x - px)) == 2:
                    d //= 2
                    rookx = max([0, d]) * 7
                    self.pieces[y][px + d] = self.pieces[y][rookx]
                    self.pieces[y][px + d].moved = True
                    self.pieces[y][rookx] = Piece()

                elif px - x == 3:
                    self.pieces[y][2] = self.pieces[y][0]
                    self.pieces[y][2].moved = True
                    self.pieces[y][0] = Piece()

            if self.pieces[y][x].piece_type != PieceType.Empty or self.pieces[py][px].piece_type == PieceType.Pawn:
                self.half = 0
            self.pieces[y][x] = self.pieces[py][px]
            self.pieces[y][x].moved = True
            self.pieces[py][px] = Piece()  # set the source piece to 0

            current = self.source_coord
            self.check = self.is_check((px, py), (x, y))
            self.source_coord = current

        self.turn *= -1
        self.half += 1
        if self.half == 50:
            self.quit = True

        if self.check and first:
            self.check_checkmate()
            self.source_coord = current

        '''
        If king is under attack, check
        For each piece
            Select piece
            If king is in highlighted cells
                check = True
                break 
        For each move opponent can make
            Make move
            If not in check anymore:
                break
        else:
            checkmate, end the game

        '''

    def check_checkmate(self):
        for row_num in range(NUM_ROWS):
            for col_num in range(NUM_ROWS):
                if self.pieces[row_num][col_num].color.value is not self.turn:
                    continue
                self.source_coord = (col_num, row_num)
                self.highlight_cells(True)
                if self.highlighted_cells != set([]):
                    return
        self.quit = True

    def knight_check(self, prev, move):
        sx, sy = tuple(add(prev, move))
        if 0 <= sx <= 7 and 0 <= sy <= 7:
            piece = self.pieces[sy][sx]
            if piece.piece_type is PieceType.Knight and piece.color.value is self.turn:
                return True
        return False

    def line_check(self, king, prev, direction):
        self.source_coord = add(prev, direction)
        while 0 <= self.source_coord[0] <= 7 and 0 <= self.source_coord[1] <= 7:
            cx, cy = self.source_coord
            if self.pieces[cy][cx].color.value == self.turn * -1:
                return False
            if self.pieces[cy][cx].color.value != 0:
                self.highlight_cells()
                if king in self.highlighted_cells:
                    return True
                return False
            self.source_coord = add(self.source_coord, direction)
        return False

    def is_check(self, prev=None, current=None):
        # maybe only checking col row diagonals of king will be faster
        # change to only check relevant pieces on board
        if self.turn == 1:
            king = self.black_king
        else:
            king = self.white_king
        if prev is None:
            prev = king

        if current is not None:
            # check if piece moved puts in check
            self.source_coord = current
            self.highlight_cells()
            if king in self.highlighted_cells:
                return True
        else:
            knight_move = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for move in knight_move:
                if self.knight_check(prev, move):
                    return True

        px, py = prev
        # check column
        if king[0] == px:
            for y, piece in enumerate([row[px] for row in self.pieces]):
                if piece.color.value is not self.turn:
                    continue
                self.source_coord = (px, y)
                self.highlight_cells()
                if king in self.highlighted_cells:
                    return True

        # check row
        if king[1] == py:
            for x, piece in enumerate(self.pieces[py]):
                if piece.color.value is not self.turn:
                    continue
                self.source_coord = (x, py)
                self.highlight_cells()
                if king in self.highlighted_cells:
                    return True

        directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
        for direction in directions:
            if self.line_check(king, prev, direction):
                return True
        return False

    def evaluate(self):
        if self.quit:
            if self.check:
                return self.turn * -9999999
            return 0

        e = 0
        for y, row in enumerate(self.pieces):
            for x, piece in enumerate(row):
                weight = tables[piece.color][piece.piece_type][y][x]
                e += piece.color.value * (piece.piece_type.value + weight)
        return e

    def copy_board(self):
        new_board = copy(self)
        new_board.pieces = [[Piece(piece=piece) for piece in row] for row in self.pieces]
        return new_board