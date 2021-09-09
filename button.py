from constants import *
import pygame

pygame.init()


class Button:
    def __init__(self, x):
        self.x = x * CLENGTH * 2
        self.y = 700
        self.width = TLENGTH // 4
        self.height = CLENGTH
        self.color = BCOLOR

    def draw(self):
        pass

    def check_hover(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.height:
            self.color = BCOLOR2
        else:
            self.color = BCOLOR
