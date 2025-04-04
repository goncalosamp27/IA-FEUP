import pygame, sys
from button import Button
from game import start_game  
from utils import get_font, draw_microphone_icon, SCREEN, BG, CLICK_SOUND
from stats import game_stats


def play(is_ai = 0):
    selected_level = 1
    selected_difficulty = 'easy'

    while True:
        SCREEN.blit(BG, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_TEXT = get_font(45).render("Choose Level and Difficulty", True, "#99afd7")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        LEVEL_TEXT = get_font(30).render(f"Level: {selected_level}", True, "White")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        DIFFICULTY_TEXT = get_font(30).render(f"Difficulty: {selected_difficulty.capitalize()}", True, "White")
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(640, 300))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        LEVEL_UP_BUTTON = Button(image=None, pos=(800, 200), 
                                 text_input=">", font=get_font(30), base_color="#6888be", hovering_color="White")
        LEVEL_DOWN_BUTTON = Button(image=None, pos=(480, 200), 
                                   text_input="<", font=get_font(30), base_color="#6888be", hovering_color="White")

        DIFFICULTY_UP_BUTTON = Button(image=None, pos=(940, 300), 
                                      text_input=">", font=get_font(30), base_color="#6888be", hovering_color="White")
        DIFFICULTY_DOWN_BUTTON = Button(image=None, pos=(340, 300), 
                                        text_input="<", font=get_font(30), base_color="#6888be", hovering_color="White")

        START_BUTTON = Button(image=None, pos=(640, 450), 
                              text_input="START", font=get_font(50), base_color="#6888be", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 640), 
                             text_input="Back", font=get_font(40), base_color="#99afd7", hovering_color="White")

        LEVEL_UP_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        LEVEL_UP_BUTTON.update(SCREEN)
        LEVEL_DOWN_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        LEVEL_DOWN_BUTTON.update(SCREEN)
        DIFFICULTY_UP_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        DIFFICULTY_UP_BUTTON.update(SCREEN)
        DIFFICULTY_DOWN_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        DIFFICULTY_DOWN_BUTTON.update(SCREEN)
        START_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        START_BUTTON.update(SCREEN)
        BACK_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_UP_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    selected_level = min(selected_level + 1, 5)
                if LEVEL_DOWN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    selected_level = max(selected_level - 1, 1)
                if DIFFICULTY_UP_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    selected_difficulty = 'medium' if selected_difficulty == 'easy' else 'hard' if selected_difficulty == 'medium' else 'easy'
                if DIFFICULTY_DOWN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    selected_difficulty = 'medium' if selected_difficulty == 'hard' else 'easy' if selected_difficulty == 'medium' else 'hard'
                if START_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    start_game(selected_level, selected_difficulty, is_ai)
                if BACK_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    main_menu()

        pygame.display.update()

def choose_ai():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("COMPUTER", True, "#ccdbee")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        AI_1_BUTTON = Button(image=None, pos=(640, 240), text_input="Greedy", font=get_font(50), base_color="#99afd7", hovering_color="White")
        AI_2_BUTTON = Button(image=None, pos=(640, 340), text_input="DFS", font=get_font(50), base_color="#99afd7", hovering_color="White")
        AI_3_BUTTON = Button(image=None, pos=(640, 440), text_input="BFS", font=get_font(50), base_color="#99afd7", hovering_color="White")
        AI_4_BUTTON = Button(image=None, pos=(640, 540), text_input="A*", font=get_font(50), base_color="#99afd7", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 650), text_input="Back", font=get_font(40), base_color="#99afd7", hovering_color="White")
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
                    CLICK_SOUND.play()
                        # Handle easy AI selection
                    print("AI1 selected")  # You can start the game with easy AI
                    play(1)
                if AI_2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                        # Handle medium AI selection
                    print("AI2 selected")  # You can start the game with medium AI
                    play(2)
                if AI_3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                        # Handle hard AI selection
                    print("AI3 selected")  # You can start the game with hard AI
                    play(3)
                if AI_4_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                        # Handle hard AI selection
                    print("AI4 selected")  # You can start the game with hard AI
                    play(4)
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                    main_menu()  # Go back to the main menu

            pygame.display.update()

def how_to_play():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("pink")
        SCREEN.blit(BG, (0, 0))

        # Title Text: "How to Play"
        TITLE_TEXT = get_font(100).render("HOW TO PLAY", True, "#FFFFFF")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)

        # Instruction Text: Explanation of Jelly Field Game
        INSTRUCTION_TEXT = get_font(25).render("Jelly field is about merging Jellies!", True, "#FFFFFF")
        INSTRUCTION_TEXT_RECT = INSTRUCTION_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_TEXT_RECT)

        INSTRUCTION_TEXT2 = get_font(20).render("Merge Jellies of the same color to make them explode!", True, "#FFFFFF")
        INSTRUCTION_TEXT_RECT2 = INSTRUCTION_TEXT2.get_rect(center=(640, 270))
        SCREEN.blit(INSTRUCTION_TEXT2, INSTRUCTION_TEXT_RECT2)

        INSTRUCTION_TEXT3 = get_font(20).render("You must explode Jellies of the colors in the objective", True, "#FFFFFF")
        INSTRUCTION_TEXT_RECT3 = INSTRUCTION_TEXT3.get_rect(center=(640, 340))
        SCREEN.blit(INSTRUCTION_TEXT3, INSTRUCTION_TEXT_RECT3)

        INSTRUCTION_TEXT4 = get_font(20).render("If the whole map is filled with Jellies, you lose :(", True, "#FFFFFF")
        INSTRUCTION_TEXT_RECT4 = INSTRUCTION_TEXT4.get_rect(center=(640, 410))
        SCREEN.blit(INSTRUCTION_TEXT4, INSTRUCTION_TEXT_RECT4)

        INSTRUCTION_TEXT5 = get_font(25).render("Have fun :D", True, "#FFFFFF")
        INSTRUCTION_TEXT_RECT5 = INSTRUCTION_TEXT5.get_rect(center=(640, 480))
        SCREEN.blit(INSTRUCTION_TEXT5, INSTRUCTION_TEXT_RECT5)

        # Button for Back: Allows going back to the main menu
        BACK_BUTTON = Button(image=None, pos=(640, 600), 
                             text_input="Back", font=get_font(50), base_color="#99afd7", hovering_color="White")
        
        BACK_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        # Event handling: If the back button is clicked, go back to main menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    CLICK_SOUND.play()
                    main_menu()

        # Update the display
        pygame.display.update()


def win_screen(is_ai = 0):
    while True:
        SCREEN.blit(BG, (0, 0)) 

        WIN_TEXT = get_font(100).render("YOU WIN!", True, "#99ff99")
        WIN_RECT = WIN_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(WIN_TEXT, WIN_RECT)

        REPLAY_BUTTON = Button(image=None, pos=(640, 500), 
                               text_input="PLAY AGAIN", font=get_font(50), base_color="#99afd7", hovering_color="White")
        MENU_BUTTON = Button(image=None, pos=(640, 600), 
                             text_input="MAIN MENU", font=get_font(50), base_color="#99afd7", hovering_color="White")

        # testing--------------
        ALGO_TEXT = get_font(30).render(f"Algorithm: {game_stats.algorithm}", True, "White")
        ALGO_RECT = ALGO_TEXT.get_rect(center=(640, 280))
        SCREEN.blit(ALGO_TEXT, ALGO_RECT)

        MOVES_TEXT = get_font(30).render(f"Moves: {game_stats.moves}", True, "White")
        MOVES_RECT = MOVES_TEXT.get_rect(center=(640, 320))
        SCREEN.blit(MOVES_TEXT, MOVES_RECT)

        TIME_TEXT = get_font(30).render(f"Time: {game_stats.duration}s", True, "White")
        TIME_RECT = TIME_TEXT.get_rect(center=(640, 360))
        SCREEN.blit(TIME_TEXT, TIME_RECT)

        if game_stats.depth:
            DEPTH_TEXT = get_font(30).render(f"Depth: {game_stats.depth}", True, "White")
            DEPTH_RECT = DEPTH_TEXT.get_rect(center=(640, 400))
            SCREEN.blit(DEPTH_TEXT, DEPTH_RECT)
        # testing--------------
        
        for button in [REPLAY_BUTTON, MENU_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    CLICK_SOUND.play()
                    play(is_ai)  
                if MENU_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    CLICK_SOUND.play()
                    main_menu()  

        pygame.display.update()
        
        
def game_over_screen(is_ai = 0):
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
                    CLICK_SOUND.play()
                    play(is_ai)  
                if MENU_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    CLICK_SOUND.play()
                    main_menu() 

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("JELLY FIELD", True, "#6888be")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="PLAY", font=get_font(60), base_color="#ccdbee", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(640, 350), 
                            text_input="COMPUTER", font=get_font(60), base_color="#ccdbee", hovering_color="White")
        HTP_BUTTON = Button(image=None, pos=(640, 450), 
                            text_input="HOW TO PLAY", font=get_font(60), base_color="#ccdbee", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 640), 
                            text_input="EXIT", font=get_font(60), base_color="#99afd7", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        draw_microphone_icon()

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, HTP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                    play()  # Trigger the game menu
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                    choose_ai()
                if HTP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                    how_to_play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    CLICK_SOUND.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
