from board import Board
from drawer import Drawer
from button import Button
from constants import *
import pyperclip
from ai import AI
import json


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


def main():
    import pygame
    pygame.init()
    try:
        with open("settings.json", "r") as read_file:
            data = json.load(read_file)
    except FileNotFoundError:
        data = {"depth": 4, "lcolor": [240, 230, 220],
                "rcolor": [199, 117, 61],
                "mcolor": [220, 173, 140],
                "scolor": [0, 255, 255],
                "hrcolor": [0, 181, 98],
                "hlcolor": [0, 255, 150],
                "bcolor": [179, 0, 255],
                "bcolor2": [217, 128, 255],
                "mtcolor": [255, 0, 0],
                "fps": 60
                }

    try:
        depth = data["depth"]
    except KeyError:
        depth = 4
        data["depth"] = depth

    try:
        fps = data["fps"]
    except KeyError:
        fps = 60
        data["fps"] = fps

    try:
        button_color = data["bcolor"]
    except KeyError:
        button_color = [179, 0, 255]
        data["bcolor"] = button_color

    try:
        bg_color = data["mcolor"]
    except KeyError:
        bg_color = [220, 173, 140]
        data["mcolor"] = bg_color

    try:
        highlight_button_color = data["bcolor2"]
    except KeyError:
        highlight_button_color = [179, 0, 255]
        data["bcolor2"] = highlight_button_color

    win = pygame.display.set_mode((TLENGTH, TLENGTH + CLENGTH))
    font = pygame.font.SysFont("Comic Sans MS", 30)

    piece_names = ["b", "k", "n", "p", "q", "r"]
    images = {i: pygame.transform.scale(pygame.image.load("images/black/" + i + ".png"), (CLENGTH, CLENGTH)) for i in
              piece_names}
    images.update(
        {i.upper(): pygame.transform.scale(pygame.image.load("images/white/" + i.upper() + ".png"), (CLENGTH, CLENGTH))
         for i in piece_names})
    ba = ["rook", "knight", "bishop", "queen"]
    nimages = {i: pygame.transform.scale(pygame.image.load("images/" + i + ".png"), (CLENGTH, CLENGTH)) for i in ba}
    drawer = Drawer(win, data, font, pygame, images, nimages)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess by Ismail Choudhury")
    title = pygame.font.SysFont("Comic Sans MS", 70)
    normal = pygame.font.SysFont("Comic Sans MS", 30)

    board = None
    ai = None
    running = True
    option = 0

    fen_buttons = [
        Button(450, 200, 100, 50, 7, "FEN", button_color, highlight_button_color),  # FEN AI button
        Button(450, 500, 100, 50, 8, "FEN", button_color, highlight_button_color)  # FEN player button
    ]
    buttons = [
        Button(100, 200, 300, 50, 1, "New Game vs AI", button_color, highlight_button_color),  # new game button
        Button(100, 300, 300, 50, 3, "Continue Game", button_color, highlight_button_color),  # continue game button
        Button(100, 400, 300, 50, 4, "Settings", button_color, highlight_button_color),  # continue game button
        Button(100, 500, 300, 50, 6, "New Game vs Player", button_color, highlight_button_color)  # continue game button
    ]

    _quit = Button(525, 600, 75, 75, 2, "Quit", button_color, highlight_button_color)  # quit button

    settings = [
        Button(300, 200, 50, 50, 4, "-", button_color, highlight_button_color),  # decrease depth
        Button(400, 200, 50, 50, 5, "+", button_color, highlight_button_color)  # increase depth
    ]

    end = Button(100, 100, 450, 50, 9, "", button_color, highlight_button_color)

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
            win.fill(bg_color)
            text = title.render("Chess", True, (0, 0, 0))
            win.blit(text, (TLENGTH // 2 - 100, 100))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    values = [button.click(*pos) for button in buttons]
                    values += [button.click(*pos) for button in fen_buttons]
                    if (x := max(values)) >= 0:
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
                drawer.draw_button(button)
            for button in fen_buttons:
                drawer.draw_button(button)

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
                    if board.half == 50:
                        end.text += ". 50 move rule"

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
                drawer.draw_button(end)
            drawer.draw_button(_quit)

        # New game
        elif option in (1, 6, 7, 8):
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
            win.fill(bg_color)
            text = title.render("Settings", True, (0, 0, 0))
            win.blit(text, (TLENGTH // 2 - 150, 100))
            depth_text = normal.render(f"difficulty = {depth}", True, (0, 0, 0))
            win.blit(depth_text, (100, 200))

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
                drawer.draw_button(button)
            drawer.draw_button(_quit)

        pygame.display.flip()
        clock.tick(fps)

    data["depth"] = depth
    with open("settings.json", "w") as file:
        json.dump(data, file, indent=2)
    pygame.quit()


if __name__ == "__main__":
    main()
