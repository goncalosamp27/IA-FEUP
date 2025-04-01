import pygame
import sys
import menu
from button import Button 
from gamestate import GameState
from jelly import Jelly

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))


BG = pygame.image.load("assets/Background7.png") 

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def win_screen():
    while True:
        SCREEN.blit(BG, (0, 0)) 

        WIN_TEXT = get_font(100).render("YOU WIN!", True, "#99ff99")
        WIN_RECT = WIN_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(WIN_TEXT, WIN_RECT)

        REPLAY_BUTTON = Button(image=None, pos=(640, 350), 
                               text_input="PLAY AGAIN", font=get_font(50), base_color="#99afd7", hovering_color="White")
        MENU_BUTTON = Button(image=None, pos=(640, 450), 
                             text_input="MAIN MENU", font=get_font(50), base_color="#99afd7", hovering_color="White")

        for button in [REPLAY_BUTTON, MENU_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    menu.CLICK_SOUND.play()
                    menu.play()  
                if MENU_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    menu.CLICK_SOUND.play()
                    menu.main_menu()  

        pygame.display.update()
        
        
def game_over_screen():
    while True:
        SCREEN.blit(BG, (0, 0))  

        GAME_OVER_TEXT = get_font(100).render("GAME OVER", True, "#ff6666")
        GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(GAME_OVER_TEXT, GAME_OVER_RECT)

        REPLAY_BUTTON = Button(image=None, pos=(640, 350), 
                               text_input="TRY AGAIN", font=get_font(50), base_color="#99afd7", hovering_color="White")
        MENU_BUTTON = Button(image=None, pos=(640, 450), 
                             text_input="MAIN MENU", font=get_font(50), base_color="#99afd7", hovering_color="White")

        for button in [REPLAY_BUTTON, MENU_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    menu.CLICK_SOUND.play()
                    menu.play()  
                if MENU_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    menu.CLICK_SOUND.play()
                    menu.main_menu() 

        pygame.display.update()


def start_game(level, difficulty):
    level_path = f'levels/level{level}.txt'
    game_state = GameState(level_path, difficulty)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        PLAY_BACK = Button(image=None, pos=(640, 680), 
                           text_input="Back", font=get_font(30), base_color="White", hovering_color="#99afd7")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        game_state.draw_board(SCREEN)
        game_state.update_scheduled_actions()


        if game_state.check_game_win():
            print("Returning to menu after win")
            win_screen()
            return
        elif game_state.check_game_over():
            print("Returning to menu after loss")
            game_over_screen()
            return

        if not game_state.is_board_normalized() and not game_state.scheduled_actions:
            game_state.schedule_board_normalization_sequence()
            print("Not Normalizado")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state.scheduled_actions:
                    continue  # ignorar inputs até finalizar açoes (isto é banger)
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

                                    print("Normalizado")
                                    break

        pygame.display.update()
