from board import Board
import drawer
from button import Button
from constants import *
import pyperclip


# 3k4/8/8/8/8/4R3/1K5p/8 testing AI promoting - possibly working
# https://www.youtube.com/watch?v=6r_VKSdpRH8
# rnbqk1nr/ppp2ppp/8/4P3/1BP5/8/PP3pPP/RN1QKBNR testing yt vid - move king up 1
# 3k4/R7/8/8/8/4R3/7p/2RK4 second testing - working
# 8/7P/8/5k2/8/8/8/1K6 testing user promoting - working
# 8/5P2/2b5/4k3/8/8/1K6/8 testing user promoting 2 - working
# 4k2r/R7/8/8/8/8/8/3R1R2 testing castling for ai - working - Does know how to castle
# 5k2/8/8/2r5/8/P2Q4/1K2p1Q1/8 testing decision making with castling
# rnbqk1nr/pppppp1p/6P1/8/8/8/PPPPPP1P/RNBQKBNR new bug - fixed
# 1nb1kb1r/2p1rppp/p4n2/1p6/2pqPB2/2N2BQ1/PP3PPP/R3R1K1 testing is_check speed improvement
# 8/1RP5/N1P5/1b2P3/k2Br3/4Pp1K/5p1b/5N2 w - - 0 1 new bug
# 3kq3/8/8/8/8/8/8/3K4 check

def main(depth):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess by Ismail Choudhury")
    title = pygame.font.SysFont("Comic Sans MS", 70)
    normal = pygame.font.SysFont("Comic Sans MS", 30)

    board = None
    running = True
    option = 0

    buttons = [
        Button(100, 200, 300, 50, 1, "New Game vs AI"),  # new game button
        Button(100, 300, 300, 50, 3, "Continue Game"),  # continue game button
        Button(100, 400, 300, 50, 4, "Settings"),  # continue game button
        Button(100, 500, 300, 50, 6, "New Game vs Player"),  # continue game button
        Button(450, 200, 100, 50, 7, "FEN from clipboard")  # FEN AI button
    ]

    _quit = Button(525, 600, 75, 75, 2, "Quit")  # quit button

    settings = [
        Button(300, 200, 50, 50, 4, "-"),  # decrease depth
        Button(400, 200, 50, 50, 5, "+")  # increase depth
    ]

    # game loop
    # 0 ... Menu
    # 1 ... Game
    # 2 ... Quit
    # 3 ... New game vs AI
    # 4 ... -1 depth
    # 5 ... +1 depth
    # 6 ... New game vs player
    # 7 ... new game vs ai with fen

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
                    if (x := max(vals)) >= 0:
                        option = x

                for button in buttons:
                    button.check_hover(*pos)

            for button in buttons:
                button.draw()

        # continue Game
        elif option == 3:
            if board is None:
                option = 0
                continue
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
            _quit.draw()

        # New game
        elif option == 1 or option == 6 or option == 7:
            if option == 1:
                board = Board(depth=depth)
            elif option == 6:
                board = Board(depth=0)
            elif option == 7:
                board = Board(string=pyperclip.paste(), depth=depth)
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
