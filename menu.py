import pygame, sys
from button import Button
from game import start_game  # Import start_game directly from game.py

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jelly Field Menu")

BG = pygame.image.load("assets/Background.png")

selected_board = None
selected_level = None
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    choose_board()  # Let the user choose the board

def choose_board():
    global selected_board
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("SELECT BOARD", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        BOARD_1_BUTTON = Button(image=None, pos=(640, 200), 
                            text_input="Board 1", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BOARD_2_BUTTON = Button(image=None, pos=(640, 300), 
                            text_input="Board 2", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BOARD_3_BUTTON = Button(image=None, pos=(640, 400), 
                            text_input="Board 3", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BOARD_4_BUTTON = Button(image=None, pos=(640, 500), 
                            text_input="Board 4", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BOARD_5_BUTTON = Button(image=None, pos=(640, 600), 
                            text_input="Board 5", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 700), 
                            text_input="Back", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [BOARD_1_BUTTON, BOARD_2_BUTTON, BOARD_3_BUTTON, BOARD_4_BUTTON, BOARD_5_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOARD_1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_board = "Board 1"
                    choose_level()  # Proceed to choose the level after selecting the board
                if BOARD_2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_board = "Board 2"
                    choose_level()
                if BOARD_3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_board = "Board 3"
                    choose_level()
                if BOARD_4_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_board = "Board 4"
                    choose_level()
                if BOARD_5_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_board = "Board 5"
                    choose_level()
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()  # Go back to the main menu

        pygame.display.update()
def choose_level():
    global selected_level
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("SELECT LEVEL", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        EASY_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="Easy", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MEDIUM_BUTTON = Button(image=None, pos=(640, 350), 
                            text_input="Medium", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HARD_BUTTON = Button(image=None, pos=(640, 450), 
                            text_input="Hard", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 550), 
                            text_input="Back", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_level = "Easy"
                    start_game()  # Start the game after selecting both board and level
                if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_level = "Medium"
                    start_game()
                if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_level = "Hard"
                    start_game()
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    choose_board()  # Go back to board selection

        pygame.display.update()
        
        
def choose_ai():
    while True:
        """
        # a pagina original
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        """
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("SELECT COMPUTER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        AI_1_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="AI 1", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        AI_2_BUTTON = Button(image=None, pos=(640, 350), 
                            text_input="AI 2", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        AI_3_BUTTON = Button(image=None, pos=(640, 450), 
                            text_input="AI 3", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        AI_4_BUTTON = Button(image=None, pos=(640, 550), 
                            text_input="AI 4", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 650), 
                            text_input="Back", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [AI_1_BUTTON, AI_2_BUTTON, AI_3_BUTTON, AI_4_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AI_1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Handle easy AI selection
                    print("Easy AI selected")  # You can start the game with easy AI
                    choose_board()
                if AI_2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Handle medium AI selection
                    print("Medium AI selected")  # You can start the game with medium AI
                    choose_board()
                if AI_3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Handle hard AI selection
                    print("Hard AI selected")  # You can start the game with hard AI
                    choose_board()
                if AI_4_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Handle hard AI selection
                    print("Hard AI selected")  # You can start the game with hard AI
                    choose_board()
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()  # Go back to the main menu

        pygame.display.update()
        
def how_to_play():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("HOW TO PLAY screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(640, 350), 
                            text_input="COMPUTER", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HTP_BUTTON = Button(image=None, pos=(640, 450), 
                            text_input="How To Play", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 650), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, HTP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Trigger the game
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    choose_ai()
                if HTP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    how_to_play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
