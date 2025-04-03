import pygame, sys, menu
from button import Button 
from gamestate import GameState
from jelly import Jelly
from utils import SCREEN, BG, get_font
import copy

def value(game_state):
    best_score = float('-inf')
    best_move = None

    for y, row in enumerate(game_state.board):
        for x, cell in enumerate(row):
            if cell == ' ':  # Only consider empty slots
                for jelly in game_state.playable_jellies:
                    score = game_state.simulate_move(x, y, jelly)
                    if score is not None and score > best_score:
                        best_score = score
                        best_move = (x, y, jelly)

    return best_move

def dfs(game_state, depth, max_depth):
    if depth == max_depth or game_state.check_game_win() or game_state.check_game_over():
        return game_state.evaluate_state()

    best_score = float('-inf')

    for jelly_index in range(len(game_state.playable_jellies)):
        for y, row in enumerate(game_state.board):
            for x, cell in enumerate(row):
                if cell == ' ':
                    simulated = copy.deepcopy(game_state)
                    jelly = simulated.playable_jellies[jelly_index]

                    if simulated.make_move(x, y, jelly):
                        simulated.schedule_board_normalization_sequence()
                        simulated.reconstruct_all()

                        score = dfs(simulated, depth + 1, max_depth)
                        best_score = max(best_score, score)

    return best_score


def dfs_best_move(game_state, max_depth):
    best_score = float('-inf')
    best_move = None

    for jelly_index in range(len(game_state.playable_jellies)):
        for y, row in enumerate(game_state.board):
            for x, cell in enumerate(row):
                if cell == ' ':
                    simulated = copy.deepcopy(game_state)
                    jelly = simulated.playable_jellies[jelly_index]  # usa a jelly equivalente no clone

                    if simulated.make_move(x, y, jelly):
                        simulated.schedule_board_normalization_sequence()
                        simulated.reconstruct_all()

                        score = dfs(simulated, 1, max_depth)

                        print(f"Testing move at ({x}, {y}) with jelly index {jelly_index} → score: {score}")

                        if score > best_score or best_move is None:
                            best_score = score
                            best_move = (x, y, jelly_index)

    return best_move

def start_game(level, difficulty, is_ai=0):
    level_path = f'levels/level{level}.txt'
    game_state = GameState(level_path, difficulty)

    if is_ai: print("AI selecionada: ", is_ai)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        PLAY_BACK = Button(image=None, pos=(640, 680), text_input="Back", font=get_font(30), base_color="White", hovering_color="#99afd7")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        game_state.draw_board(SCREEN)
        game_state.update_scheduled_actions()

        if not game_state.is_board_normalized() and not game_state.scheduled_actions:
            game_state.schedule_board_normalization_sequence()
            print("Not Normalized")

        if game_state.is_board_normalized():
            if game_state.check_game_win():
                menu.win_screen(is_ai)
                return
            elif game_state.check_game_over():
                menu.game_over_screen(is_ai)
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if is_ai == 1:  # GREEDY
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        return  # Go back to the menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if game_state.is_board_normalized() and not game_state.scheduled_actions:
                        best_move = value(game_state)  
                        if best_move:
                            x, y, jelly = best_move
                            game_state.make_move(x, y, jelly)
                            print(f"AI played move at ({x}, {y}) with jelly {jelly}")

            if is_ai == 2: # DFS
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if game_state.is_board_normalized() and not game_state.scheduled_actions:
                        best_move = dfs_best_move(game_state, max_depth=2)
                        if best_move:
                            x, y, jelly_index = best_move
                            jelly = game_state.playable_jellies[jelly_index]  

                            game_state.make_move(x, y, jelly)
                            print(f"DFS -> jelly {jelly_index} na posição ({x},{y})")

            if is_ai == 3: #BFS
                break

            if is_ai == 4: # A *
                break

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
                                            print("Normalized")
                                        break

        pygame.display.update()
