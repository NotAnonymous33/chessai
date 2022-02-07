from constants import *

class Button:
    def __init__(self, x, y, width, height, ret, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BCOLOR
        self.return_value = ret
        self.text = text
        self.is_hover = False

    def check_hover(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            self.color = BCOLOR2
            self.is_hover = True
        else:
            self.color = BCOLOR
            self.is_hover = False

    def click(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return self.return_value
        return -1
