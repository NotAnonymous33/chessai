from constants import *
from timer import timer
import concurrent.futures
import dis

# https://stackoverflow.com/questions/6785226/pass-multiple-parameters-to-concurrent-futures-executor-map


class AI:
    def __init__(self, depth):
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
        lowest_eval = 99999999
        best_move = None
        promoting = False
        for row in range(NUM_ROWS)[::-1]:
            for col in range(NUM_ROWS)[::-1]:
                print(col, row)
                if board.pieces[row][col].color.value != -1:
                    continue
                board.reset_source()
                board.source_coord = (col, row)
                board.highlight_cells(True)

                highlighted = list(board.highlighted_cells)
                if not len(highlighted):
                    continue
                print(highlighted)

                for move in highlighted:
                    temp_board = board.copy_board()
                    temp_board.move_piece(*move, True)

                    # if promoting then need to add some stuff here
                    # make sure to do that
                    # causes big unexpected problems
                    # took a while to figure out this was the source of those problems
                    if temp_board.promote:
                        for promoting_move in temp_board.highlighted_cells:
                            promoting_temp_board = temp_board.copy_board()
                            promoting_temp_board.move_piece(*promoting_move, True)
                            promoting_eval = self.minimax(promoting_temp_board, self.depth, True)
                            if promoting_eval < lowest_eval:
                                lowest_eval = promoting_eval
                                best_source = (col, row)
                                best_move = move
                                promoting = True
                                best_promoting_move = promoting_move

                    # add for if pawn y = 0
                    # add castling
                    else:
                        evaluation = self.minimax(temp_board, self.depth, True)
                        if evaluation < lowest_eval:
                            lowest_eval = evaluation
                            best_source = (col, row)
                            best_move = move
                            promoting = False

        print(lowest_eval)
        board.source_coord = best_source
        board.move_piece(*best_move, True)
        if promoting:
            board.move_piece(*best_promoting_move, True)
        board.reset_source()

    # def get_eval(self, move, board):
    #     temp_board = pickle.loads(pickle.dumps(board, -1))
    #     temp_board.move_piece(*move)
    #     return self.minimax(temp_board, self.depth, True)

    # @cache
    # @lru_cache(maxsize=None)
    def minimax(self, board, depth, white, alpha=-99999999, beta=99999999) -> int:
        """
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

        """
        #if board in self.saved.keys():
         #   return self.saved[board]

        if not depth:
            return board.evaluate()
        # do stuff
        val = [-1, 1][white]  # val = 1 if white else -1
        board.turn = val

        if white:
            max_eval = -99999999
            for rowy in range(NUM_ROWS)[::-1]:
                for colx in range(NUM_ROWS)[::-1]:
                    if board.pieces[rowy][colx].color.value == val:
                        board.reset_source()
                        board.source_coord = (colx, rowy)
                        board.highlight_cells(True)

                        for move in board.highlighted_cells:
                            temp_board = board.copy_board()
                            temp_board.move_piece(*move, True)
                            if temp_board.promote:
                                highest_promoting_eval = -99999999
                                for promoting_move in temp_board.highlighted_cells:
                                    promoting_temp_board = temp_board.copy_board()
                                    promoting_temp_board.move_piece(*promoting_move, True)
                                    promoting_eval = self.minimax(promoting_temp_board, 1, white, alpha, beta)
                                    if promoting_eval > highest_promoting_eval:
                                        highest_promoting_eval = promoting_eval
                                eval = highest_promoting_eval
                            elif temp_board.quit:
                                eval = temp_board.evaluate()
                            else:
                                eval = self.minimax(temp_board, depth - 1, not white, alpha, beta)

                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                return max_eval
            return max_eval

        # if not white
        min_eval = 99999999
        for rowy in range(NUM_ROWS)[::-1]:
            for colx in range(NUM_ROWS)[::-1]:
                if board.pieces[rowy][colx].color.value == val:
                    board.reset_source()
                    board.source_coord = (colx, rowy)
                    board.highlight_cells(True)

                    for move in board.highlighted_cells:
                        temp_board = board.copy_board()
                        temp_board.move_piece(*move, True)
                        if temp_board.promote:
                            lowest_promoting_eval = 99999999
                            for promoting_move in temp_board.highlighted_cells:
                                promoting_temp_board = temp_board.copy_board()
                                promoting_temp_board.move_piece(*promoting_move, True)
                                promoting_eval = self.minimax(promoting_temp_board, 1, white, alpha, beta)
                                if promoting_eval < lowest_promoting_eval:
                                    lowest_promoting_eval = promoting_eval
                            eval = lowest_promoting_eval
                        elif temp_board.quit:
                            eval = temp_board.evaluate()
                        else:
                            eval = self.minimax(temp_board, depth - 1, not white, alpha, beta)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            return min_eval
        return min_eval

        # # https://www.youtube.com/watch?v=l-hh51ncgDI
        # # depth is not 0
        # evals = []
        # for rowy in range(NUM_ROWS):
        #     for colx in range(NUM_ROWS):
        #         if board.pieces[rowy][colx].color.value == val:
        #             board.reset_source()
        #             board.source_coord = (colx, rowy)
        #             board.highlight_cells(True)
        #
        #             for move in board.highlighted_cells:
        #                 temp_board = board.copy_board()
        #                 temp_board.move_piece(*move, True)
        #                 evals.append(self.minimax(temp_board, depth - 1, not white))
        # if not len(evals):
        #     return 0
        # if white:
        #     return max(evals)
        # return min(evals)
