from constants import *
import pygame


normal = pygame.font.SysFont("Comic Sans MS", 30)

class Button:
    def __init__(self, x, y, width, height, ret, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BCOLOR
        self.return_value = ret
        self.text = text

    def draw(self):
        pygame.draw.rect(WIN, self.color, [self.x, self.y, self.width, self.height])
        WIN.blit(normal.render(self.text, True, (0, 0, 0)), (self.x + 5, self.y))

    def check_hover(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            self.color = BCOLOR2
        else:
            self.color = BCOLOR

    def click(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return self.return_value
        return -1
