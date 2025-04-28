from collections import deque
import copy

def count_objective(state):
    total_count = 0

    for i in range(1, 4):
        count_key = f"count{i}"
        if count_key in state.objective:
            total_count += state.objective[count_key]
    return total_count

def compare_game_states(estado_simulado, estado_atual):
    # quanto maior a diferença melhor
    total_simulado = count_objective(estado_simulado)
    total_atual = count_objective(estado_atual)
    
    return total_atual - total_simulado

def get_possible_moves(state): # retirar as posições vazias
    moves = []
    i = 0
    for y, row in enumerate(state.board):
        for x, cell in enumerate(row):
            if cell == ' ':  
                i += 1
                moves.append((x, y))
	
    return moves

def dfs(state, depth):
    if depth == 0 or state.check_game_over():
        return None, 0, 1  # nada a fazer

    best_score = -float('inf')
    best_action = None  
    
    states_generated = 0  

    for jelly_index in range(len(state.playable_jellies)):
        for x, y in get_possible_moves(state):
            simulated_state = copy.deepcopy(state)
            simulated_jelly = simulated_state.playable_jellies[jelly_index]
                        
            if simulated_state.make_move(x, y, simulated_jelly):
                
                simulated_state.normalize_board()
                simulated_state.reconstruct_all()

                progresso = compare_game_states(simulated_state, state)
                _, future_score, generated_states = dfs(simulated_state, depth - 1)
                
                states_generated += generated_states

                if progresso == 0 and future_score == 0:
                    total_score = -10  # penalizar jogadas inúteis 
                else: total_score = progresso + future_score

                if total_score > best_score:
                    best_score = total_score
                    best_action = (x, y, jelly_index)

    return best_action, best_score, states_generated

def bfs(state, max_depth=2):
    queue = deque()
    best_score = -float('inf')
    best_action = None  
    states_generated = 0 

    for jelly_index in range(len(state.playable_jellies)):
        for x, y in get_possible_moves(state):

            initial_state = copy.deepcopy(state)
            jelly = initial_state.playable_jellies[jelly_index]

            if initial_state.make_move(x, y, jelly):
                initial_state.normalize_board()
                initial_state.reconstruct_all()

                progresso = compare_game_states(initial_state, state)

                queue.append((initial_state, (x, y, jelly_index), 1, progresso))

                states_generated += 1 
                  
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

                    states_generated += 1
                    
                    if total_score > best_score:
                        best_score = total_score
                        best_action = initial_action

    return best_action, best_score, states_generated
