import random
import pygame
from jelly import Jelly

class GameState:
    def __init__(self, level_file, difficulty):
        self.board = self.load_board(level_file)
        self.difficulty = difficulty
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
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == '_':
                    pygame.draw.rect(screen, (0, 0, 0), (x * Jelly.SIZE, y * Jelly.SIZE, Jelly.SIZE, Jelly.SIZE))
                elif cell == ' ':
                    pygame.draw.rect(screen, (255, 255, 255), (x * Jelly.SIZE, y * Jelly.SIZE, Jelly.SIZE, Jelly.SIZE))
                elif isinstance(cell, Jelly):
                    cell.set_position(x * Jelly.SIZE, y * Jelly.SIZE)
                    cell.draw(screen)
