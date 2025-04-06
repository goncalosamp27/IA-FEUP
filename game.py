import pygame, sys, menu, time, tracemalloc, os
from button import Button 
from gamestate import GameState
from jelly import Jelly
from utils import get_font, SCREEN, BG, CLICK_SOUND, HINT_SOUND, JELLY_SOUND
from informedsearch import value, a_star
from uninformedsearch import dfs, bfs

def start_game(level, difficulty, is_ai=0):
    level_path = f'levels/level{level}.txt'
    game_state = GameState(level_path, difficulty)

    hint_move = None
    hint_start_time = None

    # --- AI Performance Tracking ---
    ai_start_time = time.time()
    tracemalloc.start()
    ai_moves = []

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        PLAY_BACK = Button(image=None, pos=(640, 680), text_input="Back", font=get_font(30), base_color="White", hovering_color="#99afd7")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        if is_ai == 0:  # Human mode
            HINT_BUTTON = Button(image=None, pos=(640, 550), text_input="Hint", font=get_font(30), base_color="White", hovering_color="#99afd7")
            HINT_BUTTON.changeColor(PLAY_MOUSE_POS)
            HINT_BUTTON.update(SCREEN)

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
                # --- Save AI result on game end ---
                if is_ai:
                    ai_end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    elapsed_time = ai_end_time - ai_start_time
                    memory_kb = peak / 1024
                    result = "Victory" if game_state.check_game_win() else "Loss"
                    algorithm_name = {
                        1: "Greedy",
                        2: "DFS",
                        3: "BFS",
                        4: "A*",
                        5: "WeightedA*"
                    }[is_ai]

                    output_folder = "results"
                    os.makedirs(output_folder, exist_ok=True)

                    # Include difficulty in the filename
                    log_filename = os.path.join(output_folder, f"{algorithm_name}_level{level}_{difficulty}.txt")
                    json_filename = os.path.join(output_folder, f"{algorithm_name}_level{level}_{difficulty}.json")

                    # Save game state as JSON
                    game_state.save_to_file(json_filename)

                    # Save readable log with a separator between executions
                    with open(log_filename, "a") as f:  # Open in append mode ('a')
                        f.write(f"Algorithm: {algorithm_name}\n")
                        f.write(f"Level: {level}\n")
                        f.write(f"Difficulty: {difficulty}\n")
                        f.write(f"Time Taken: {elapsed_time:.4f} seconds\n")
                        f.write(f"Memory Used: {memory_kb:.2f} KB\n")
                        f.write(f"Number of States Generated: {states_generated}\n")
                        f.write(f"Result: {result}\n")
                        f.write(f"Total Moves: {len(ai_moves)}\n\n")

                        f.write("Moves:\n")
                        for move in ai_moves:
                            f.write(f"{move}\n")

                        f.write(f"\nFull game state saved to: {json_filename}\n")

                        # Add separator for next execution
                        f.write("\n===========\n")

                menu.win_screen(is_ai)
                return

            elif game_state.check_game_over():
                # --- Save AI result on game end ---
                if is_ai:
                    ai_end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    elapsed_time = ai_end_time - ai_start_time
                    memory_kb = peak / 1024
                    result = "Victory" if game_state.check_game_win() else "Loss"
                    algorithm_name = {
                        1: "Greedy",
                        2: "DFS",
                        3: "BFS",
                        4: "A*",
                        5: "WeightedA*"
                    }[is_ai]

                    output_folder = "results"
                    os.makedirs(output_folder, exist_ok=True)

                    # Include difficulty in the filename
                    log_filename = os.path.join(output_folder, f"{algorithm_name}_level{level}_{difficulty}.txt")
                    json_filename = os.path.join(output_folder, f"{algorithm_name}_level{level}_{difficulty}.json")

                    # Save game state as JSON
                    game_state.save_to_file(json_filename)

                    # Save readable log with a separator between executions
                    with open(log_filename, "a") as f:  # Open in append mode ('a')
                        f.write(f"Algorithm: {algorithm_name}\n")
                        f.write(f"Level: {level}\n")
                        f.write(f"Difficulty: {difficulty}\n")
                        f.write(f"Time Taken: {elapsed_time:.4f} seconds\n")
                        f.write(f"Memory Used: {memory_kb:.2f} KB\n")
                        f.write(f"Number of States Generated: {states_generated}\n")
                        f.write(f"Result: {result}\n")
                        f.write(f"Total Moves: {len(ai_moves)}\n\n")

                        f.write("Moves:\n")
                        for move in ai_moves:
                            f.write(f"{move}\n")

                        f.write(f"\nFull game state saved to: {json_filename}\n")

                        # Add separator for next execution
                        f.write("\n===========\n")
                        f.write("\n")

                menu.game_over_screen(is_ai)
                return

        if is_ai > 0 and game_state.is_board_normalized() and not game_state.scheduled_actions:
            if is_ai == 1:  # GREEDY
                best_move, states_generated = value(game_state)
                if best_move:
                    x, y, jelly = best_move
                    game_state.make_move(x, y, jelly)
                    ai_moves.append(("Greedy", (x, y), jelly.to_dict()))
                    print(f"AI played move at ({x}, {y}) with jelly {jelly}")

            elif is_ai == 2:  # DFS
                best_action, _, states_generated = dfs(game_state, 2)
                x, y, jelly_index = best_action
                jelly = game_state.playable_jellies[jelly_index]
                game_state.make_move(x, y, jelly)
                ai_moves.append(("DFS", (x, y), jelly.to_dict()))
                print(f"DFS -> jelly {jelly_index} em ({x}, {y})")

            elif is_ai == 3:  # BFS
                best_action, _, states_generated = bfs(game_state, 2)
                x, y, jelly_index = best_action
                jelly = game_state.playable_jellies[jelly_index]
                game_state.make_move(x, y, jelly)
                ai_moves.append(("BFS", (x, y), jelly.to_dict()))
                print(f"BFS -> jelly {jelly_index} em ({x}, {y})")

            elif is_ai == 4:  # A*
                best_move, states_generated = a_star(game_state, 2, False)
                if best_move:
                    x, y, jelly = best_move
                    game_state.make_move(x, y, jelly)
                    ai_moves.append(("A*", (x, y), jelly.to_dict()))
                    print(f"A* played move at ({x}, {y}) with jelly {jelly}")

            elif is_ai == 5:  # Weighted A*
                best_move = a_star(game_state, 2, True)
                if best_move:
                    x, y, jelly = best_move
                    game_state.make_move(x, y, jelly)
                    ai_moves.append(("Weighted A*", (x, y), jelly.to_dict()))
                    print(f"A* played move at ({x}, {y}) with jelly {jelly}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if is_ai == 0:  # Human Mode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_state.scheduled_actions:
                        continue  # Ignore inputs until actions are finished
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        return  # Go back to the menu
                    if HINT_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        HINT_SOUND.play()
                        hint_move = value(game_state)
                        hint_start_time = time.time()
                        continue

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
