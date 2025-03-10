import pygame
import sys
from button import Button  # Import Button for UI interactions
from gamestate import GameState

# Removed import of main_menu to avoid circular imports
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

BG = pygame.image.load("assets/Background.png") 

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def start_game():
    game_state = GameState('levels/level1.txt', 'easy')

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

        pygame.display.update()
        
