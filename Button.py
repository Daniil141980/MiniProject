import pygame

pygame.init()


class Button:
    def __init__(self, width, height, x, y, message):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.inactive = (13, 162, 58)
        self.active = (23, 204, 58)
        self.message = message

    def draw(self, display, click):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            pygame.draw.rect(display, self.active, (self.x, self.y, self.width, self.height))
            if click:
                return 1
            return 0
        else:
            pygame.draw.rect(display, self.inactive, (self.x, self.y, self.width, self.height))
            return 0
