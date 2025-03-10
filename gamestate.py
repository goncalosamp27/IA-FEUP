import random
import pygame
from jelly import Jelly

class GameState:
    COLORS = ['#be2528', '#2536be', '#7525be', '#3eb34b', '#64bfbe', '#e2d614'] # red, blue, purple, green, cyan, yellow

    def __init__(self, level_file, difficulty):
        self.board = self.load_board(level_file)
        self.difficulty = difficulty
        self.objective = self.generate_objective()  
        self.randomize_jellies()

    def load_board(self, level_file):
        with open(level_file, 'r') as file:
            board = [list(line.strip()) for line in file.readlines()]
        return board

    def randomize_jellies(self):
        for row in self.board:
            for i in range(len(row)):
                if row[i] == 'X':
                    # Randomly choose between a playable empty space (' ') or a jelly
                    if random.choice([True, False]):
                        row[i] = ' '  # Playable empty space
                    else:
                        jelly = Jelly(0, 0, None, None, None, None)
                        jelly.set_random_colors()
                        row[i] = jelly

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
                if cell == '':
                    pygame.draw.rect(screen, (0, 0, 0), (draw_x, draw_y, Jelly.SIZE, Jelly.SIZE))
                elif cell == ' ':
                    pygame.draw.rect(screen, (255, 255, 255), (draw_x, draw_y, Jelly.SIZE, Jelly.SIZE))
                elif isinstance(cell, Jelly):
                    cell.set_position(draw_x, draw_y)
                    cell.draw(screen)

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