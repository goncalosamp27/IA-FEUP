import pygame, sys, menu, time
from button import Button 
from gamestate import GameState
from jelly import Jelly
from utils import get_font, SCREEN, BG, CLICK_SOUND, JELLY_SOUND
from informedsearch import value, a_star_best_move
from dfsbfs import dfs, bfs
# from dfsbfs import dfs2

def test_ai(level, difficulty, is_ai=0, is_test=True):
    level_path = f'levels/level{level}.txt'
    game_state = GameState(level_path, difficulty, is_ai=is_ai, is_test=is_test)

    hint_move = None
    hint_start_time = None
    
    if is_ai: print("Test_AI selecionada: ", is_ai)
    if is_test: print("Test_AI selecionada: ", is_test)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        PLAY_BACK = Button(image=None, pos=(640, 680), text_input="Back", font=get_font(30), base_color="White", hovering_color="#99afd7")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        game_state.draw_board(SCREEN, hint_move)
        game_state.update_scheduled_actions()

        if hint_start_time and time.time() - hint_start_time > 5:
            hint_move = None
            hint_start_time = None

        if not game_state.is_board_normalized() and not game_state.scheduled_actions:
            game_state.schedule_board_normalization_sequence()
            print("Not Normalized")

        if game_state.is_board_normalized():
            if game_state.check_game_win():
                menu.win_screen(test_ai)
                return
            elif game_state.check_game_over():
                menu.game_over_screen(test_ai)
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if is_ai == 1:  # GREEDY
                print("Entrou no TESTE GREEDY")
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        return  # Go back to the menu
                    else:
                        continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if game_state.is_board_normalized() and not game_state.scheduled_actions:
                        best_move = value(game_state)  
                        if best_move:
                            x, y, jelly = best_move
                            game_state.make_move(x, y, jelly)
                            print(f"AI played move at ({x}, {y}) with jelly {jelly}")

            if is_ai == 2:  # DFS
                print("Entrou no TESTE DFS")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        return  # Go back to the menu
                    else:
                        continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if game_state.is_board_normalized() and not game_state.scheduled_actions:
                        best_action, _ = dfs(game_state, 2)
                        # versao goofy # best_action, _ = dfs2(game_state)

                        x, y, jelly_index = best_action
                        jelly = game_state.playable_jellies[jelly_index]

                        game_state.make_move(x, y, jelly)
                        print(f"DFS -> jelly {jelly_index} em ({x}, {y})")

            if is_ai == 3: #BFS
                print("Entrou no TESTE BFS")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        return  # Go back to the menu
                    else:
                        continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if game_state.is_board_normalized() and not game_state.scheduled_actions:
                        best_action, _ = bfs(game_state, 2)

                        x, y, jelly_index = best_action
                        jelly = game_state.playable_jellies[jelly_index]

                        game_state.make_move(x, y, jelly)
                        print(f"BFS -> jelly {jelly_index} em ({x}, {y})")

            if is_ai == 4: # A *
                print("Entrou no TESTE A*")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        return  # Go back to the menu
                    else:
                        continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if game_state.is_board_normalized() and not game_state.scheduled_actions:
                        best_move = a_star_best_move(game_state)  # Use A* to find the best move
                        if best_move:
                            x, y, jelly = best_move
                            game_state.make_move(x, y, jelly)
                            print(f"A* played move at ({x}, {y}) with jelly {jelly}")

            if is_ai == 5: # Iterative Deepening
                break

            else:  # Human Mode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_state.scheduled_actions:
                        continue  # Ignore inputs until actions are finished
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        return  # Go back to the menu

                    # Handle jelly selection
                    for jelly in game_state.playable_jellies:
                        jelly_x, jelly_y = jelly.get_position()
                        if jelly_x <= PLAY_MOUSE_POS[0] <= jelly_x + Jelly.SIZE and jelly_y <= PLAY_MOUSE_POS[1] <= jelly_y + Jelly.SIZE:
                            CLICK_SOUND.play()
                            game_state.select_jelly(jelly)
                            break

                    # Handle jelly placement
                    if game_state.selected_jelly:
                        for y, row in enumerate(game_state.board):
                            for x, cell in enumerate(row):
                                if cell == ' ':
                                    draw_x = x * Jelly.SIZE + (SCREEN.get_width() - len(game_state.board[0]) * Jelly.SIZE) // 2
                                    draw_y = y * Jelly.SIZE + (SCREEN.get_height() - len(game_state.board) * Jelly.SIZE) // 2 - 100
                                    if draw_x <= PLAY_MOUSE_POS[0] <= draw_x + Jelly.SIZE and draw_y <= PLAY_MOUSE_POS[1] <= draw_y + Jelly.SIZE:
                                        if game_state.make_move(x, y, game_state.selected_jelly):
                                            JELLY_SOUND.play()
                                            hint_move = None  
                                            hint_start_time = None
                                            print("Normalized")
                                        break

        pygame.display.update()
