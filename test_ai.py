import pygame, sys, menu, time
from button import Button 
from gamestate import GameState
from informedsearch import value, a_star_best_move
from dfsbfs import dfs, bfs
from stats import game_stats

import time
import sys
import os
import csv

def test_ai(selected_algorithm, selected_map, selected_difficulty):
    print(f"Testando {['Greedy', 'DFS', 'BFS', 'A*'][selected_algorithm - 1]} no mapa {selected_map} com dificuldade {selected_difficulty}")

    level_file = f"levels/level{selected_map}.txt"

    game_state = GameState(selected_map, selected_algorithm, selected_difficulty, True)
    game_state.set_fixed_jellies_positions(level_file)

    # Initialize game_stats with required metrics
    game_stats.reset()
    game_stats.algorithm = ["Greedy", "DFS", "BFS", "A*"][selected_algorithm - 1]
    game_stats.states_generated = 0  # Start tracking states
    game_stats.max_memory_used = 0  # Track max memory usage

    start_time = time.time()

    while not game_state.check_game_win() and not game_state.check_game_over():
        if not game_state.is_board_normalized() or game_state.scheduled_actions:
            game_state.schedule_board_normalization_sequence()
            game_state.update_scheduled_actions()
            continue

        if selected_algorithm == 1:  # Algoritmo Greedy
            best_move = value(game_state)
            if best_move:
                x, y, jelly = best_move
                game_state.make_move(x, y, jelly)
                game_stats.moves += 1

                # Track states and memory usage
                game_stats.states_generated += 1
                memory_usage = sys.getsizeof(game_state)
                game_stats.max_memory_used = max(game_stats.max_memory_used, memory_usage)

        elif selected_algorithm == 2:  # Algoritmo DFS
            best_action, _ = dfs(game_state, 2)
            if best_action is None:
                break
            x, y, jelly_index = best_action
            jelly = game_state.playable_jellies[jelly_index]
            game_state.make_move(x, y, jelly)
            game_stats.moves += 1

            # Track states and memory usage
            game_stats.states_generated += 1
            memory_usage = sys.getsizeof(game_state)
            game_stats.max_memory_used = max(game_stats.max_memory_used, memory_usage)

        elif selected_algorithm == 3:  # Algoritmo BFS
            best_action, _ = bfs(game_state, 2)
            if best_action is None:
                break
            x, y, jelly_index = best_action
            jelly = game_state.playable_jellies[jelly_index]
            game_state.make_move(x, y, jelly)
            game_stats.moves += 1

            # Track states and memory usage
            game_stats.states_generated += 1
            memory_usage = sys.getsizeof(game_state)
            game_stats.max_memory_used = max(game_stats.max_memory_used, memory_usage)

        elif selected_algorithm == 4:  # Algoritmo A*
            best_move = a_star_best_move(game_state)
            if best_move:
                x, y, jelly = best_move
                game_state.make_move(x, y, jelly)
                game_stats.moves += 1
            else:
                break

            # Track states and memory usage
            game_stats.states_generated += 1
            memory_usage = sys.getsizeof(game_state)
            game_stats.max_memory_used = max(game_stats.max_memory_used, memory_usage)

    # Registra o tempo total de execução do teste
    total_time = time.time() - start_time
    game_stats.time = round(total_time, 3)

    # Salva os resultados em um arquivo CSV
    result_row = [
        game_stats.algorithm,
        selected_map,
        selected_difficulty,
        game_stats.moves,
        game_stats.time,
        game_stats.states_generated,
        game_stats.max_memory_used,
        "Yes" if game_state.check_game_win() else "No"
    ]

    # Cria a pasta para armazenar os resultados e escreve no arquivo CSV
    os.makedirs("results", exist_ok=True)
    csv_path = "results/ai_test_results.csv"
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow([
                "Algorithm", "Level", "Difficulty", "Moves", "Time", 
                "States Generated", "Max Memory Used", "Win"
            ])  # Cabeçalho
        writer.writerow(result_row)

    print("Resultados salvos no CSV ✅")
    print(f"Movimentos: {game_stats.moves}, Tempo: {game_stats.time:.3f}s, Estados Gerados: {game_stats.states_generated}, Memória Máxima: {game_stats.max_memory_used} bytes, Vitória: {result_row[-1]}")
