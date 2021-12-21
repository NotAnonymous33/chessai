from board import Board
from constants import *
import drawer
from button import Button


pygame.init()


def main():
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess by Ismail Choudhury")
    title = pygame.font.SysFont("Comic Sans MS", 70)
    normal = pygame.font.SysFont("Comic Sans MS", 30)

    board = Board()

    running = True
    option = 0

    buttons = []
    buttons.append(Button(100, 200, 200, 50, 1))
    quit = Button(525, 600, 75, 75, 2)
    x = 0

    # game loop
    while running:
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


        elif option == 1:
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

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()


pygame.quit()





