from collections import deque
import copy

def count_objective(state):
    total_count = 0

    for i in range(1, 4):
        count_key = f"count{i}"
        if count_key in state.objective:
            total_count += state.objective[count_key]
    print(f"[count_objective] Estado atual do objetivo: {state.objective}")
    return total_count

def compare_game_states(estado_simulado, estado_atual):
    # quanto maior a diferença melhor
    total_simulado = count_objective(estado_simulado)
    total_atual = count_objective(estado_atual)
    
    return total_atual - total_simulado

def get_possible_moves(state): # retirar as posições vazias
    moves = []
    i = 0
    print("MOVES POSSÍVEIS!\n")
    for y, row in enumerate(state.board):
        for x, cell in enumerate(row):
            if cell == ' ':  
                i += 1
                moves.append((x, y))
                print(f"{i}: ({x}, {y})")
	
    return moves

def dfs(state, depth):
    if depth == 0 or state.check_game_over():
        return None, 0  # nada a fazer

    best_score = -float('inf')
    best_action = None  

    for jelly_index in range(len(state.playable_jellies)):
        for x, y in get_possible_moves(state):
            simulated_state = copy.deepcopy(state)
            simulated_jelly = simulated_state.playable_jellies[jelly_index]
            
            print(f"Jelly {jelly_index} em ({x}, {y})")
            
            if simulated_state.make_move(x, y, simulated_jelly):
                
                simulated_state.normalize_board()
                simulated_state.reconstruct_all()

                progresso = compare_game_states(simulated_state, state)
                _, future_score = dfs(simulated_state, depth - 1)

                if progresso == 0 and future_score == 0:
                    total_score = -10  # penalizar jogadas inúteis (?) -> nao sei se devemos por isto, mas escolhe melhor a jogada
                else: total_score = progresso + future_score

                print(f"Progress: {progresso}") 
                print(f"Possível Futuro: {future_score}") 

                if total_score > best_score:
                    best_score = total_score
                    best_action = (x, y, jelly_index)

                print(f"SCORE: {total_score}") 

    return best_action, best_score

def bfs(state, max_depth=2):
    queue = deque()
    best_score = -float('inf')
    best_action = None  

    for jelly_index in range(len(state.playable_jellies)):
        for x, y in get_possible_moves(state):

            initial_state = copy.deepcopy(state)
            jelly = initial_state.playable_jellies[jelly_index]

            if initial_state.make_move(x, y, jelly):
                initial_state.normalize_board()
                initial_state.reconstruct_all()

                progresso = compare_game_states(initial_state, state)

                queue.append((initial_state, (x, y, jelly_index), 1, progresso))

                if progresso > best_score:
                    best_score = progresso
                    best_action = (x, y, jelly_index)

    while queue:
        current_state, initial_action, depth, score_so_far = queue.popleft()

        if depth >= max_depth or current_state.check_game_over():
            continue

        for jelly_index in range(2):
            for x, y in get_possible_moves(current_state):

                next_state = copy.deepcopy(current_state)
                jelly = next_state.playable_jellies[jelly_index]

                if next_state.make_move(x, y, jelly):
                    next_state.normalize_board()
                    next_state.reconstruct_all()
                    progresso = compare_game_states(next_state, current_state)
                    total_score = score_so_far + progresso

                    queue.append((next_state, initial_action, depth + 1, total_score))

                    if total_score > best_score:
                        best_score = total_score
                        best_action = initial_action

    return best_action, best_score

"""
def dfs2(state):
    best_score = -float('inf')
    best_action = None  # (x, y, jelly_index)

    for first_index in range(2):  # 0 (A) ou 1 (B)
        second_index = 1 - first_index

        for x1, y1 in get_possible_moves(state):
            first_state = copy.deepcopy(state)
            jelly_first = first_state.playable_jellies[first_index]

            if first_state.make_move(x1, y1, jelly_first):
                first_state.normalize_board()
                first_state.reconstruct_all()
                progresso_1 = compare_game_states(first_state, state)

                # Segunda jogada com a jelly que sobrou no mesmo índice
                for x2, y2 in get_possible_moves(first_state):
                    second_state = copy.deepcopy(first_state)
                    jelly_second = second_state.playable_jellies[second_index]

                    if second_state.make_move(x2, y2, jelly_second):
                        second_state.normalize_board()
                        second_state.reconstruct_all()
                        progresso_2 = compare_game_states(second_state, first_state)

                        total_score = progresso_1 + progresso_2

                        print(f"Jelly {first_index} em ({x1},{y1}) → depois jelly {second_index} em ({x2},{y2}) | Total: {total_score}")

                        if total_score > best_score:
                            best_score = total_score
                            best_action = (x1, y1, first_index)

    return best_action, best_score
"""