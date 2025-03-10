import random
import pygame

class Jelly:
    COLORS = ['#be2528', '#2536be', '#7525be', '#3eb34b', '#64bfbe', '#e2d614'] # red, blue, purple, green, cyan, yellow
    SIZE = 80

    def __init__(self, posX, posY, tl, tr, bl, br):
        self.posX = posX
        self.posY = posY
        self.tl = tl # top left
        self.tr = tr # top right
        self.bl = bl # bottom left
        self.br = br # bottom right

    def get_position(self):
        return self.posX, self.posY

    def set_position(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def set_corner_color(self, tl, tr, bl, br):
        self.tl = tl
        self.tr = tr
        self.bl = bl
        self.br = br

    def set_random_colors(self):
        self.tl = random.choice(self.COLORS)
        self.tr = random.choice(self.COLORS)
        self.bl = random.choice(self.COLORS)
        self.br = random.choice(self.COLORS)

    def get_colors(self):
        return self.tl, self.tr, self.bl, self.br

    def draw(self, screen, size=None):
        if size is None:
            size = self.SIZE
        x, y = self.posX, self.posY

        pygame.draw.rect(screen, self.tl, (x, y, size // 2, size // 2)) # Top-left
        pygame.draw.rect(screen, self.tr, (x + size // 2, y, size // 2, size // 2)) # Top-right
        pygame.draw.rect(screen, self.bl, (x, y + size // 2, size // 2, size // 2)) # Bottom-left
        pygame.draw.rect(screen, self.br, (x + size // 2, y + size // 2, size // 2, size // 2)) # Bottom-right