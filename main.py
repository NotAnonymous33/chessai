from board import Board
import drawer
from button import Button
from constants import *




def main():
    global DEPTH
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess by Ismail Choudhury")
    title = pygame.font.SysFont("Comic Sans MS", 70)
    normal = pygame.font.SysFont("Comic Sans MS", 30)

    board = Board()

    running = True
    option = 0

    buttons = []
    buttons.append(Button(100, 200, 300, 50, 1, "New Game"))  # new game button
    buttons.append(Button(100, 300, 300, 50, 3, "Continue Game"))  # continue game button
    buttons.append(Button(100, 400, 300, 50, 4, "Settings"))  # continue game button
    quit = Button(525, 600, 75, 75, 2, "Quit")  # quit button
    x = 0

    settings = []
    settings.append(Button(300, 200, 50, 50, 4, "-"))
    settings.append(Button(400, 200, 50, 50, 5, "+"))
    # settings.append(Button(100, 400, 300, 50, 4, "3"))


    # game loop
    # 0 ... Menu
    # 1 ... Game
    # 2 ... Quit
    # 3 ... New game
    # 4 ... -1 depth
    # 5 ... +1 depth
    # 6 ...

    while running:
        # Menu
        if option == 0:
            WIN.fill(MCOLOR)
            text = title.render("Chess", True, (0, 0, 0))
            WIN.blit(text, (TLENGTH//2 - 100, 100))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT or board.check_quit():
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    vals = [button.click(*pos) for button in buttons]
                    if (x := max(vals)) >= 0:
                        option = x

                for button in buttons:
                    button.check_hover(*pos)

            for button in buttons:
                button.draw()

        # Game
        elif option == 3:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT or board.check_quit():
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    board.click(*pos)
                    if quit.click(*pos) == 2:
                        option = 0

                quit.check_hover(*pos)

            drawer.draw(board)
            quit.draw()

        # New game
        elif option == 1:
            print(DEPTH)
            board = Board(DEPTH)
            option = 3

        # Settings
        elif option == 4:
            WIN.fill(MCOLOR)
            text = title.render("Settings", True, (0, 0, 0))
            WIN.blit(text, (TLENGTH // 2 - 150, 100))
            depth_text = normal.render(f"{DEPTH = }", True, (0, 0, 0))
            WIN.blit(depth_text, (100, 200))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT or board.check_quit():
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if quit.click(*pos) == 2:
                        option = 0
                    # check for button presses
                    for button in settings:
                        if (val := button.click(*pos)) != -1:
                            if val == 4:
                                DEPTH -= 1
                            elif val == 5:
                                DEPTH += 1


                for button in settings:
                    button.check_hover(*pos)
                quit.check_hover(*pos)

            for button in settings:
                button.draw()
            quit.draw()


        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()


pygame.quit()





