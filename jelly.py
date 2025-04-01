import random
import pygame

class Jelly:
    #COLORS = ['#be2528', '#2536be', '#7525be', '#3eb34b', '#64bfbe', '#e2d614'] # red, blue, purple, green, cyan, yellow
    
    #COLORS = ['#f7b7b7',  # Soft pastel red
    #      '#a2c7e0',  # Soft pastel blue
    #      '#d1a1e7',  # Soft pastel purple
     #     '#b6e4b1',  # Soft pastel green
     #     '#a4d9d3',  # Soft pastel cyan
     #     '#f9f2a1']  # Soft pastel yellow
     
    COLORS = ['#e08b8b',  # Darker pastel red
          '#5b97c2',  # Darker pastel blue
          '#9a64c0',  # Darker pastel purple
          '#7fc57b',  # Darker pastel green
          '#5fb5ae',  # Darker pastel cyan
          '#e0c750']  # Darker pastel yellow

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

    def set_random_colors(self, avoid_colors=None):
        avoid_colors = avoid_colors or []

        valid_colors = [color for color in self.COLORS if color not in avoid_colors]

        if not valid_colors:
            valid_colors = self.COLORS  # fallback

        self.tl = random.choice(valid_colors)
        self.tr = random.choice(valid_colors)
        self.bl = random.choice(valid_colors)
        self.br = random.choice(valid_colors)


    def get_colors(self):
        return self.tl, self.tr, self.bl, self.br

    def draw(self, screen, size=None, board_color=(230, 230, 230)):
        if size is None:
            size = self.SIZE
        x, y = self.posX, self.posY

        pygame.draw.rect(screen, self.tl if self.tl is not None else (211, 211, 211),
                        (x, y, size // 2, size // 2))  
        pygame.draw.rect(screen, self.tr if self.tr is not None else (211, 211, 211),
                        (x + size // 2, y, size // 2, size // 2))  
        pygame.draw.rect(screen, self.bl if self.bl is not None else (211, 211, 211),
                        (x, y + size // 2, size // 2, size // 2))  
        pygame.draw.rect(screen, self.br if self.br is not None else (211, 211, 211),
                        (x + size // 2, y + size // 2, size // 2, size // 2))  

    def reconstruct(self):
        tl = self.tl
        tr = self.tr
        bl = self.bl 
        br = self.br
        
        corners = [tl, tr, bl, br]
        nones = sum(1 for c in corners if c is None)

        if nones == 4: return

        if nones == 3:
            existing_color = next(c for c in corners if c is not None)
            self.tl = self.tr = self.bl = self.br = existing_color
            return
        
        if nones == 2:
            if tl is not None and bl is not None:  
                self.tr = tl
                self.br = bl
            elif tr is not None and br is not None:  
                self.tl = tr
                self.bl = br
            elif tl is not None and tr is not None:  
                self.bl = tl
                self.br = tr
            elif bl is not None and br is not None:  
                self.tl = bl
                self.tr = br
            elif tl is not None and br is not None:  # diagonal TL + BR
                self.tr = tl
                self.bl = br
            elif tr is not None and bl is not None:  # diagonal TR + BL
                self.tl = tr
                self.br = bl
            return
        
        if nones == 1:
            from collections import Counter

            if self.tl is None:
                adj = [self.tr, self.bl]
            elif self.tr is None:
                adj = [self.tl, self.br]
            elif self.bl is None:
                adj = [self.tl, self.br]
            elif self.br is None:
                adj = [self.tr, self.bl]

            # Remover None e contar as cores
            color_counter = Counter(c for c in adj if c is not None)

            if color_counter:
                # Menos comum: último da lista
                color = color_counter.most_common()[-1][0]
            else:
                # fallback de segurança (deveria haver pelo menos uma cor)
                color = "#000000"

            if self.tl is None:
                self.tl = color
            elif self.tr is None:
                self.tr = color
            elif self.bl is None:
                self.bl = color
            elif self.br is None:
                self.br = color

            return

            
        

        



