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

    def reconstruct(self):
        existing_colors = [c for c in [self.tl, self.tr, self.bl, self.br] if c is not None]

        # Se todas as cores desapareceram, Jelly destruída
        if not existing_colors:
            return None  

        # Se apenas 1 cor restar, todos dessa cor
        if len(existing_colors) == 1:
            self.tl = self.tr = self.bl = self.br = existing_colors[0]
            return

        # Se 2 cantos desapareceram, preenche com a cor na vertical ou horizontal
        missing_corners = {corner: idx for idx, corner in enumerate([self.tl, self.tr, self.bl, self.br]) if corner is None}
        
        if len(missing_corners) == 2:
            if 0 in missing_corners and 1 in missing_corners:  # Top-left e Top-right desapareceram
                self.tl = self.bl  # Top-left assume Bottom-left
                self.tr = self.br  # Top-right assume Bottom-right
            elif 2 in missing_corners and 3 in missing_corners:  # Bottom-left e Bottom-right desapareceram
                self.bl = self.tl  # Bottom-left assume Top-left
                self.br = self.tr  # Bottom-right assume Top-right
            elif 0 in missing_corners and 2 in missing_corners:  # Left-side corners desapareceram
                self.tl = self.tr  # Top-left assume Top-right
                self.bl = self.br  # Bottom-left assume Bottom-right
            elif 1 in missing_corners and 3 in missing_corners:  # Right-side corners desapareceram
                self.tr = self.tl  # Top-right assume Top-left
                self.br = self.bl  # Bottom-right assume Bottom-left
            return

        # Se apenas 1 canto desapareceu, assume a cor do canto anterior no sentido anti-horário
        if self.br is None:
            self.br = self.bl  # Inferior direito assume cor do inferior esquerdo
        if self.bl is None:
            self.bl = self.tl  # Inferior esquerdo assume cor do superior esquerdo
        if self.tl is None:
            self.tl = self.tr  # Superior esquerdo assume cor do superior direito
        if self.tr is None:
            self.tr = self.br  # Superior direito assume cor do inferior direito
