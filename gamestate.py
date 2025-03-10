import random
import pygame
from jelly import Jelly

class GameState:
    def __init__(self, level_file, difficulty):
        self.board = self.load_board(level_file)
        self.difficulty = difficulty
        self.randomize_jellies()
        self.generate_playable_jellies()  # Ensure playable jellies are generated

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
        self.playable_jellies = [Jelly(0, 0, None, None, None, None), Jelly(0, 0, None, None, None, None)]
        for jelly in self.playable_jellies:
            jelly.set_random_colors()

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
                if cell == '_':
                    pygame.draw.rect(screen, (0, 0, 0), (draw_x, draw_y, Jelly.SIZE, Jelly.SIZE))  # Non-playable space
                elif cell == ' ':
                    pygame.draw.rect(screen, (211, 211, 211), (draw_x, draw_y, Jelly.SIZE, Jelly.SIZE))  # Playable space (light gray)
                elif isinstance(cell, Jelly):
                    cell.set_position(draw_x, draw_y)
                    cell.draw(screen)

        # Draw the playable jellies below the board
        jelly_y = offset_y + board_height + 50
        self.playable_jellies[0].set_position(offset_x, jelly_y)
        self.playable_jellies[1].set_position(offset_x + board_width - Jelly.SIZE, jelly_y)
        self.playable_jellies[0].draw(screen)
        self.playable_jellies[1].draw(screen)


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

        # Draw the playable jellies below the board
        jelly_y = offset_y + board_height + 50
        self.playable_jellies[0].set_position(offset_x, jelly_y)
        self.playable_jellies[1].set_position(offset_x + board_width - Jelly.SIZE, jelly_y)
        self.playable_jellies[0].draw(screen)
        self.playable_jellies[1].draw(screen)
