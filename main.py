from board import Board
import drawer
from button import Button
from constants import *
import pyperclip
from ai import AI


# 3k4/8/8/8/8/4R3/1K5p/8 testing AI promoting
# https://www.youtube.com/watch?v=6r_VKSdpRH8
# rnbqk1nr/ppp2ppp/8/4P3/1BP5/8/PP3pPP/RN1QKBNR testing yt vid - move king up 1
# 3k4/R7/8/8/8/4R3/7p/2RK4 testing promoting
# 8/7P/8/5k2/8/8/8/1K6 testing user promoting
# 8/5P2/2b5/4k3/8/8/1K6/8 testing user promoting 2
# 4k2r/R7/R7/R7/R7/R7/R7/K2R1R2 castling test with lots of rooks
# 5k2/8/8/2r5/8/P2Q4/1K2p1Q1/8 testing decision making with castling
# rnbqk1nr/pppppp1p/6P1/8/8/8/PPPPPP1P/RNBQKBNR promoting and taking piece
# 1nb1kb1r/2p1rppp/p4n2/1p6/2pqPB2/2N2BQ1/PP3PPP/R3R1K1 testing is_check speed improvement
# 8/1RP5/N1P5/1b2P3/k2Br3/4Pp1K/5p1b/5N2 w - - 0 1 new bug
# 3kq3/8/8/8/8/8/8/3K4 check
# 1k4r1/5r2/8/8/7K/8/8/8 checkmate - ai wins
# 6k1/5p2/6p1/8/7p/8/6PP/7K w - - 0 1 testing
# 8/8/8/5RB1/2pk1K2/3r4/8/8 - checkmate testing

def fen_check(string):
    string = string.split()
    if len(string) == 1 and string[0].count("/") == 7:
        return True
    if len(string) != 6 and len(string) != 2:
        return False
    if string[0].count("/") != 7:
        return False
    if string[1] != "w" and string[1] != "b":
        return False
    if len(string) == 2:
        return True
    if set(string[2]).difference(set("KQkq-")) != set([]):
        return False
    if not string[4].isdigit():
        return False
    if not string[5].isdigit():
        return False
    return True




def main(depth):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess by Ismail Choudhury")
    title = pygame.font.SysFont("Comic Sans MS", 70)
    normal = pygame.font.SysFont("Comic Sans MS", 30)

    board = None
    ai = None
    running = True
    option = 0

    fen_buttons = [
        Button(450, 200, 100, 50, 7, "FEN from clipboard"),  # FEN AI button
        Button(450, 500, 100, 50, 8, "FEN")  # FEN player button
    ]
    buttons = [
        Button(100, 200, 300, 50, 1, "New Game vs AI"),  # new game button
        Button(100, 300, 300, 50, 3, "Continue Game"),  # continue game button
        Button(100, 400, 300, 50, 4, "Settings"),  # continue game button
        Button(100, 500, 300, 50, 6, "New Game vs Player"),  # continue game button
    ]

    _quit = Button(525, 600, 75, 75, 2, "Quit")  # quit button

    settings = [
        Button(300, 200, 50, 50, 4, "-"),  # decrease depth
        Button(400, 200, 50, 50, 5, "+")  # increase depth
    ]

    end = Button(100, 100, 450, 50, 9, "")

    with open("game.txt", "w"):
        pass
    with open("pgn.txt", "w"):
        pass

    # game loop
    # 0 ... Menu
    # 1 ... Game
    # 2 ... Quit
    # 3 ... New game vs AI
    # 4 ... -1 depth
    # 5 ... +1 depth
    # 6 ... New game vs player
    # 7 ... new game vs ai with fen
    # 8 ... new game vs player with fen
    # 9 ... end of game

    while running:
        # Menu
        if option == 0:
            WIN.fill(MCOLOR)
            text = title.render("Chess", True, (0, 0, 0))
            WIN.blit(text, (TLENGTH // 2 - 100, 100))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    vals = [button.click(*pos) for button in buttons]
                    vals += [button.click(*pos) for button in fen_buttons]
                    if (x := max(vals)) >= 0:
                        option = x

                for button in buttons:
                    button.check_hover(*pos)
                for button in fen_buttons:
                    button.check_hover(*pos)
                    if button.is_hover:
                        if fen_check(pyperclip.paste()):
                            button.color = (0, 255, 0)
                        else:
                            button.color = (255, 0, 0)

            for button in buttons:
                button.draw()
            for button in fen_buttons:
                button.draw()

        # continue Game
        elif option == 3:
            if board is None:
                option = 0
                continue
            if board.quit:
                end.text = "Game has ended"
                if board.check:
                    if board.turn == -1:
                        end.text += ". White has won"
                    else:
                        end.text += ". Black has won"
                else:
                    end.text += " in stalemate"

            elif board.turn == -1 and board.ai:
                ai.move(board)

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    board.click(*pos)

                    if _quit.click(*pos) == 2:
                        option = 0

                _quit.check_hover(*pos)

            drawer.draw(board)
            if board.quit:
                end.draw()
            _quit.draw()

        # New game
        elif option == 1 or option == 6 or option == 7 or option == 8:
            if option == 1:
                board = Board(depth=depth)
                ai = AI(depth)
            elif option == 6:
                board = Board(depth=0)
            elif option == 7:
                if fen_check((string := pyperclip.paste())):
                    board = Board(string=string, depth=depth)
                    ai = AI(depth)
                else:
                    option = 0
                    continue
            elif option == 8:
                if fen_check((string := pyperclip.paste())):
                    board = Board(string=string, depth=0)
                else:
                    option = 0
                    continue
            option = 3

        # Settings
        elif option == 4:
            WIN.fill(MCOLOR)
            text = title.render("Settings", True, (0, 0, 0))
            WIN.blit(text, (TLENGTH // 2 - 150, 100))
            depth_text = normal.render(f"{depth = }", True, (0, 0, 0))
            WIN.blit(depth_text, (100, 200))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if _quit.click(*pos) == 2:
                        option = 0
                    # check for button presses
                    for button in settings:
                        if (val := button.click(*pos)) != -1:
                            if val == 4:
                                depth -= 1
                            elif val == 5:
                                depth += 1

                for button in settings:
                    button.check_hover(*pos)
                _quit.check_hover(*pos)

            for button in settings:
                button.draw()
            _quit.draw()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main(DEPTH)

pygame.quit()
