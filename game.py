import pygame
import sys
from button import Button 
from gamestate import GameState
from jelly import Jelly

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

BG = pygame.image.load("assets/Background.png") 

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        PLAY_BACK = Button(image=None, pos=(640, 680), 
                           text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        game_state.draw_board(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    return  # Go back to the menu (you can modify this to call main_menu() in menu.py)
                # Check if a playable jelly is selected
                for i, jelly in enumerate(game_state.playable_jellies):
                    jelly_x, jelly_y = jelly.get_position()
                    if jelly_x <= PLAY_MOUSE_POS[0] <= jelly_x + Jelly.SIZE and jelly_y <= PLAY_MOUSE_POS[1] <= jelly_y + Jelly.SIZE:
                        game_state.select_jelly(jelly)
                        break
                # Check if a playable slot is clicked
                if game_state.selected_jelly:
                    for y, row in enumerate(game_state.board):
                        for x, cell in enumerate(row):
                            if cell == ' ':
                                draw_x = x * Jelly.SIZE + (SCREEN.get_width() - len(game_state.board[0]) * Jelly.SIZE) // 2
                                draw_y = y * Jelly.SIZE + (SCREEN.get_height() - len(game_state.board) * Jelly.SIZE) // 2 - 100
                                if draw_x <= PLAY_MOUSE_POS[0] <= draw_x + Jelly.SIZE and draw_y <= PLAY_MOUSE_POS[1] <= draw_y + Jelly.SIZE:
                                    game_state.board[y][x] = game_state.selected_jelly
                                    game_state.replace_played_jelly(game_state.selected_jelly)
                                    game_state.selected_jelly = None
                                    break

        pygame.display.update()