import random
import pygame
from jelly import Jelly

class GameState:
    COLORS = ['#be2528', '#2536be', '#7525be', '#3eb34b', '#64bfbe', '#e2d614']  # red, blue, purple, green, cyan, yellow

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
                if cell == '_':
                    pygame.draw.rect(screen, (0, 0, 0), (draw_x, draw_y, Jelly.SIZE, Jelly.SIZE))  # Non-playable space
                elif cell == ' ':
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

    def select_jelly(self, jelly):
        self.selected_jelly = None if self.selected_jelly == jelly else jelly