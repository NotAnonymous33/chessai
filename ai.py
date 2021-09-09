from copy import copy
from constants import *
from random import choice
from timer import timer


class AI:
    def __init__(self, depth=1):
        self.depth = depth - 1

    @timer
    def move(self, board):
        # find the best move and move it

        """
        ________________________________________
        |Actual stuff which is meant to happen
        ---------------------------------------
        | 1. For each piece
        | 2. For each move the piece can make
        | 3. Evaluate this position
        | 4. If the position is higher than the current valued position
        | 5. Set the source coord as the best source coord
        | 6. Set the dest coord as the best dest coord
        | 7. After evaluating all moves, move the piece from src to dest
        ------------------------------------------
        Loop through pieces using x y range
        If black set this as temp coord
        Check highlighted cells
        For each highlighted cell, create new board copy and move cell from temp coord to highlighted cell
        Evaluate position
        If evaluated position is higher than current evaluation, set best coords
        Move the piece
        """
        best_source = (0, 0)
        lowest_eval = 50
        best_move = None
        for row in range(NUM_ROWS):
            for col in range(NUM_ROWS):
                if board.pieces[row][col].color.value != -1:
                    continue
                board.reset_source()
                board.source_coord = (col, row)
                board.highlight_cells(True)

                for move in board.highlighted_cells:
                    temp_board = board.copyboard()
                    temp_board.move_piece(*move)

                    # add for if pawn y = 0
                    # add castling

                    if self.depth == 0:
                        evaluation = temp_board.evaluate()
                    else:
                        evaluation = self.minimax(temp_board, self.depth, True)

                    if evaluation < lowest_eval:
                        lowest_eval = evaluation
                        best_source = (col, row)
                        best_move = move

        # dear future me, instead of making board, try doing board = temp_board in above for loop
        board.source_coord = best_source
        board.move_piece(*best_move)

    def minimax(self, board, depth, white) -> int:
        '''
        white value = 1
        black value = 0
        create a list, return a value
        if depth == 1:
            for every piece make every move
            create list of eval
            if white return highest
            otherwise return lowest
        else:
            x = []
            for each piece make every move
            x.append(minimax(board, depth - 1, not white))
            if white return highest
            else return lowest

        '''
        # do stuff
        val = 1 if white else -1
        if depth == 1:
            evals = []
            for rowy in range(NUM_ROWS):
                for colx in range(NUM_ROWS):
                    if board.pieces[rowy][colx].color.value == val:
                        board.reset_source()
                        board.source_coord = (colx, rowy)
                        board.highlight_cells(True)

                        for move in board.highlighted_cells:
                            temp_board = board.copyboard()
                            temp_board.move_piece(*move)
                            evals.append(temp_board.evaluate())
            if not len(evals):
                return 0
            if white:
                return max(evals)
            return min(evals)

        # depth is not 1
        evals = []
        for rowy in range(NUM_ROWS):
            for colx in range(NUM_ROWS):
                if board.pieces[rowy][colx].color.value == val:
                    board.reset_source()
                    board.source_coord = (colx, rowy)
                    board.highlight_cells(True)

                    for move in board.highlighted_cells:
                        temp_board = board.copyboard()
                        temp_board.move_piece(*move)
                        evals.append(self.minimax(temp_board, depth - 1, not white))
        if not len(evals):
            return 0
        if white:
            return max(evals)
        return min(evals)




