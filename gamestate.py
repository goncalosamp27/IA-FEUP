import random
import pygame
from jelly import Jelly

class GameState:
    #COLORS = ['#be2528', '#2536be', '#7525be', '#3eb34b', '#64bfbe', '#e2d614']  # red, blue, purple, green, cyan, yellow
    
    #COLORS = ['#f7b7b7',  # Soft pastel red
     #     '#a2c7e0',  # Soft pastel blue
     #     '#d1a1e7',  # Soft pastel purple
     #     '#b6e4b1',  # Soft pastel green
      #    '#a4d9d3',  # Soft pastel cyan
     #     '#f9f2a1']  # Soft pastel yellow
    
    COLORS = ['#e08b8b',  # Darker pastel red
          '#5b97c2',  # Darker pastel blue
          '#9a64c0',  # Darker pastel purple
          '#7fc57b',  # Darker pastel green
          '#5fb5ae',  # Darker pastel cyan
          '#e0c750']  # Darker pastel yellow

    def __init__(self, level_file, difficulty):
        self.board = self.load_board(level_file)
        self.difficulty = difficulty
        self.objective = self.generate_objective()
        self.randomize_jellies()
        self.generate_playable_jellies()  # Ensure playable jellies are generated
        self.selected_jelly = None

    def load_board(self, level_file):
        with open(level_file, 'r') as file:
            board = [list(line.strip()) for line in file.readlines()]
        return board

    def randomize_jellies(self):
        for y, row in enumerate(self.board):
            for x in range(len(row)):
                if row[x] == 'X':
                    # Randomly choose between a playable empty space (' ') or a jelly
                    if random.choice([True, False]):
                        row[x] = ' '  # Playable empty space
                    else:
                        jelly = Jelly(0, 0, None, None, None, None)
                        self.set_unique_random_colors(jelly, y, x)
                        row[x] = jelly

    # def check_color_collisions(self):

    def set_unique_random_colors(self, jelly, y, x):
        adjacent_colors = set()
        if y > 0 and isinstance(self.board[y-1][x], Jelly):
            adjacent_colors.update(self.board[y-1][x].get_colors())
        if x > 0 and isinstance(self.board[y][x-1], Jelly):
            adjacent_colors.update(self.board[y][x-1].get_colors())

        available_colors = [color for color in Jelly.COLORS if color not in adjacent_colors]
        jelly.tl = random.choice(available_colors)
        jelly.tr = random.choice(available_colors)
        jelly.bl = random.choice(available_colors)
        jelly.br = random.choice(available_colors)

    def generate_playable_jellies(self):
        self.playable_jellies = [self.create_random_jelly(), self.create_random_jelly()]

    def create_random_jelly(self):
        jelly = Jelly(0, 0, None, None, None, None)
        jelly.set_random_colors()
        return jelly

    def replace_played_jelly(self, played_jelly):
        new_jelly = self.create_random_jelly()
        for i in range(len(self.playable_jellies)):
            if self.playable_jellies[i] == played_jelly:
                self.playable_jellies[i] = new_jelly
                break

    def generate_objective(self):
        if self.difficulty == 'easy':
            color1 = random.choice(self.COLORS)
            color2 = random.choice(self.COLORS)

            while color2 == color1:
                color2 = random.choice(self.COLORS)

            return {
                "color1": color1,
                "count1": 10,
                "color2": color2,
                "count2": 5
            }

        elif self.difficulty == 'medium':
            color1 = random.choice(self.COLORS)
            color2 = random.choice(self.COLORS)
            color3 = random.choice(self.COLORS)

            while color2 == color1:
                color2 = random.choice(self.COLORS)
            while color3 == color1 or color3 == color2:
                color3 = random.choice(self.COLORS)

            return {
                "color1": color1,
                "count1": 10,
                "color2": color2,
                "count2": 7,
                "color3": color3,
                "count3": 5
            }

        else:  # Difícil
            color1 = random.choice(self.COLORS)
            color2 = random.choice(self.COLORS)
            color3 = random.choice(self.COLORS)

            while color2 == color1:
                color2 = random.choice(self.COLORS)
            while color3 == color1 or color3 == color2:
                color3 = random.choice(self.COLORS)

            return {
                "color1": color1,
                "count1": 15,
                "color2": color2,
                "count2": 10,
                "color3": color3,
                "count3": 7
            }

    def display_board(self):
        for row in self.board:
            display_row = []
            for cell in row:
                if isinstance(cell, Jelly):
                    display_row.append('J')  # Represent jelly with 'J'
                else:
                    display_row.append(cell)
            print(' '.join(display_row))

    def draw_board(self, screen):
        board_width = len(self.board[0]) * Jelly.SIZE
        board_height = len(self.board) * Jelly.SIZE
        screen_width, screen_height = screen.get_size()

        offset_x = (screen_width - board_width) // 2
        offset_y = (screen_height - board_height) // 2 - 100

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                draw_x = x * Jelly.SIZE + offset_x
                draw_y = y * Jelly.SIZE + offset_y
                
                if cell == ' ':
                    pygame.draw.rect(screen, (211, 211, 211), (draw_x, draw_y, Jelly.SIZE, Jelly.SIZE))  # Playable space (light gray)
                elif isinstance(cell, Jelly):
                    cell.set_position(draw_x, draw_y)
                    cell.draw(screen)

        # Draw the playable jellies below the board
        jelly_y = offset_y + board_height + 50
        for i, jelly in enumerate(self.playable_jellies):
            jelly_x = offset_x if i == 0 else offset_x + board_width - Jelly.SIZE
            if jelly == self.selected_jelly:
                # Draw the selected jelly larger
                jelly.set_position(jelly_x - 10, jelly_y - 10)
                jelly.draw(screen, size=Jelly.SIZE + 20)
            else:
                jelly.set_position(jelly_x, jelly_y)
                jelly.draw(screen)

        font = pygame.font.Font("assets/font.ttf", 40)

        y_offset = 20
        for i in range(1, 4):  
            color_key = f"color{i}"
            count_key = f"count{i}"

            if color_key in self.objective and count_key in self.objective:
                color_hex = self.objective[color_key]  
                count = self.objective[count_key]  

                # Converter cor hexadecimal para RGB
                color_rgb = pygame.Color(color_hex)  

                # Criar texto com a cor correspondente
                text_surface = font.render(f"Pop {count}", True, color_rgb)
                screen.blit(text_surface, (20, y_offset))
                y_offset += 60  # Espaço entre os textos

    def select_jelly(self, jelly):
        self.selected_jelly = None if self.selected_jelly == jelly else jelly

    def check_game_over(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    
    def check_game_win(self):
        for i in range(1, 4):
            count_key = f"count{i}"
            if count_key in self.objective and self.objective[count_key] > 0:
                return False
        return True
    
    def decrement_objective(self, destroyed_color1, destroyed_color2, destroyed_color3):
        destroyed_colors = [destroyed_color1, destroyed_color2, destroyed_color3]  

        for i in range(3):  
            count_key = f"count{i+1}"

            if count_key in self.objective:
                self.objective[count_key] = max(0, self.objective[count_key] - destroyed_colors[i]) 

    def is_board_normalized(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if isinstance(self.board[y][x], Jelly):
                    jelly = self.board[y][x]

                    # Verificar colisão com a Jelly abaixo
                    if y + 1 < len(self.board) and isinstance(self.board[y + 1][x], Jelly):
                        bottom_jelly = self.board[y + 1][x]
                        if jelly.bl == bottom_jelly.tl or jelly.br == bottom_jelly.tr:
                            return False  # Ainda há colisões

                    # Verificar colisão com a Jelly à direita
                    if x + 1 < len(self.board[y]) and isinstance(self.board[y][x + 1], Jelly):
                        right_jelly = self.board[y][x + 1]
                        if jelly.tr == right_jelly.tl or jelly.br == right_jelly.bl:
                            return False  # Ainda há colisões

                    # Verificar colisão com Jelly na diagonal (inferior direita)
                    if (y + 1 < len(self.board) and x + 1 < len(self.board[y]) and 
                        isinstance(self.board[y + 1][x + 1], Jelly)):
                        diagonal_jelly = self.board[y + 1][x + 1]
                        if jelly.br == diagonal_jelly.tl:
                            return False  

        return True  

    def check_collisions_and_explode(self):        
        explosions = []  # Lista para armazenar os cantos que devem explodir

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if not isinstance(self.board[y][x], Jelly):  # Se não for uma Jelly, ignora
                    continue

                jelly = self.board[y][x]

                # Verificar colisão com a Jelly abaixo (y+1) se existir
                if y + 1 < len(self.board) and isinstance(self.board[y + 1][x], Jelly):
                    bottom_jelly = self.board[y + 1][x]
                    if jelly.bl == bottom_jelly.tl:
                        explosions.append((jelly, "bl"))
                        explosions.append((bottom_jelly, "tl"))
                    if jelly.br == bottom_jelly.tr:
                        explosions.append((jelly, "br"))
                        explosions.append((bottom_jelly, "tr"))

                # Verificar colisão com a Jelly à direita (x+1) se existir
                if x + 1 < len(self.board[y]) and isinstance(self.board[y][x + 1], Jelly):
                    right_jelly = self.board[y][x + 1]
                    if jelly.tr == right_jelly.tl:
                        explosions.append((jelly, "tr"))
                        explosions.append((right_jelly, "tl"))
                    if jelly.br == right_jelly.bl:
                        explosions.append((jelly, "br"))
                        explosions.append((right_jelly, "bl"))

                # Verificar colisão com Jelly na diagonal (inferior direita) se existir
                if y + 1 < len(self.board) and x + 1 < len(self.board[y]) and isinstance(self.board[y + 1][x + 1], Jelly):
                    diagonal_jelly = self.board[y + 1][x + 1]
                    if jelly.br == diagonal_jelly.tl:
                        explosions.append((jelly, "br"))
                        explosions.append((diagonal_jelly, "tl"))

        # Se houver pelo menos 3 explosões da mesma cor, confirmar que explodem todas
        if len(explosions) >= 3:
            for jelly_obj, corner in explosions:
                setattr(jelly_obj, corner, None)  # Define o canto como None

        # Agora reconstruímos todas as Jellies afetadas
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if isinstance(self.board[y][x], Jelly):
                    self.board[y][x].reconstruct()
