import heapq, itertools

def value(game_state):
    best_score = float('-inf')
    best_move = None

    for y, row in enumerate(game_state.board):
        for x, cell in enumerate(row):
            if cell == ' ':  
                for jelly_index in range(len(game_state.playable_jellies)):

                    jelly = game_state.playable_jellies[jelly_index]
                    score = game_state.simulate_move(x, y, jelly)
                    print(f"Colocar a Jelly {jelly_index} em {x}, {y} dá {score} pontos")
                
                    if score is not None and score > best_score:
                        best_score = score
                        best_move = (x, y, jelly)

    return best_move

counter = itertools.count()  # Unique counter to break heap ties

def heuristic(game_state):
    OBJECTIVE_WEIGHT = 500  
    remaining_goals = sum(game_state.objective.get(f"count{i}", 0) for i in range(1, 4))
    return -remaining_goals * OBJECTIVE_WEIGHT  # Lower remaining goals = better score

def a_star_best_move(game_state):
    open_set = []  # Priority queue
    best_move = None
    best_score = float('-inf')

    # Add all possible initial moves to the queue
    for y, row in enumerate(game_state.board):
        for x, cell in enumerate(row):
            if cell == ' ':  # Valid move spot
                for jelly in game_state.playable_jellies:
                    score = game_state.simulate_move(x, y, jelly)
                    
                    if score is not None:
                        g_score = score  # Use score from simulate_move()
                        h_score = heuristic(game_state)
                        f_score = g_score + h_score

                        heapq.heappush(open_set, (f_score, next(counter), (x, y, jelly), g_score))

    while open_set:
        _, _, move, g_score = heapq.heappop(open_set)

        x, y, jelly = move
        score = game_state.simulate_move(x, y, jelly)  # Simulate the move again

        if score is not None and score > best_score:
            best_score = score
            best_move = move  # Store the best move found

    return best_move