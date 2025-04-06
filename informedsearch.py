import heapq, itertools

def value(game_state):
    best_score = float('-inf')
    best_move = None
    states_generated = 0

    for y, row in enumerate(game_state.board):
        for x, cell in enumerate(row):
            if cell == ' ':  
                for jelly_index in range(len(game_state.playable_jellies)):

                    jelly = game_state.playable_jellies[jelly_index]
                    score = game_state.simulate_move(x, y, jelly)
                    states_generated += 1
                    print(f"Colocar a Jelly {jelly_index} em {x}, {y} dá {score} pontos")
                
                    if score is not None and score > best_score:
                        best_score = score
                        best_move = (x, y, jelly)

    return best_move, states_generated

counter = itertools.count()  # Unique counter to break heap ties

def heuristic(game_state, weighted=True):
    OBJECTIVE_WEIGHT = 1000
    h = 0

    for i in range(1, 4):
        count_key = f"count{i}"
        if count_key in game_state.objective and game_state.objective[count_key] > 0:
            initial_target = {
                "easy": [10, 5],
                "medium": [10, 7, 5],
                "hard": [15, 10, 7]
            }[game_state.difficulty][i - 1]
            remaining = game_state.objective[count_key]
            progress = initial_target - remaining
            
            if weighted:
                h -= remaining * OBJECTIVE_WEIGHT
                h += progress * (OBJECTIVE_WEIGHT // 2)
            else:
                h += progress - remaining

    return h

def a_star(game_state, max_depth=2, weighted=True):
    open_set = []  # Priority queue
    best_move = None
    best_score = float('-inf')
    states_generated = 0

    # Add all possible initial moves to the queue
    for y, row in enumerate(game_state.board):
        for x, cell in enumerate(row):
            if cell == ' ':  
                for jelly in game_state.playable_jellies:
                    score = game_state.simulate_move(x, y, jelly)  

                    if score is not None:
                        h_score = heuristic(game_state, weighted)  # Estimate future cost
                        f_score = score + h_score  # A* f = g + h

                        heapq.heappush(open_set, (f_score, next(counter), (x, y, jelly), score, 1))
                        states_generated += 1

    while open_set:
        _, _, move, g_score, depth = heapq.heappop(open_set)
        x, y, jelly = move

        if g_score > best_score:
            best_score = g_score
            best_move = move

        # Expand further moves if below depth limit
        if depth < max_depth:
            for y2, row in enumerate(game_state.board):
                for x2, cell in enumerate(row):
                    if cell == ' ':
                        for next_jelly in game_state.playable_jellies:
                            new_score = game_state.simulate_move(x2, y2, next_jelly)  
                            
                            if new_score is not None:
                                new_g = g_score + new_score
                                new_h = heuristic(game_state, weighted)  # Recalculate heuristic
                                new_f = new_g + new_h  # Accumulate score

                                heapq.heappush(open_set, (new_f, next(counter), (x2, y2, next_jelly), new_g, depth + 1))
                                states_generated += 1

    return best_move, states_generated