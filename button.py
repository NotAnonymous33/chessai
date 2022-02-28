class Button:
    def __init__(self, x, y, width, height, ret, text, color, hcolor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = self.default_color = color
        self.highlight_color = hcolor
        self.return_value = ret
        self.text = text
        self.is_hover = False

    def check_hover(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            self.color = self.highlight_color
            self.is_hover = True
        else:
            self.color = self.default_color
            self.is_hover = False

    def click(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return self.return_value
        return -1
