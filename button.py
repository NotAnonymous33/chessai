from constants import *
import pygame

pygame.init()


class Button:
    def __init__(self, x, y, width, height, ret):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BCOLOR
        self.return_value = ret

    def draw(self):
        pygame.draw.rect(WIN, self.color, [self.x, self.y, self.width, self.height])

    def check_hover(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            self.color = BCOLOR2
        else:
            self.color = BCOLOR

    def click(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return self.return_value
        return -1
