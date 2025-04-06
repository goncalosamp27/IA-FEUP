import heapq, itertools
import copy
from dfsbfs import compare_game_states

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

    return best_move
def iterative_deepening(game_state, max_total_depth=2, weighted=True):
     best_move = None
     best_score = float('-inf')
 
     for depth in range(1, max_total_depth + 1):
         move = a_star(game_state, max_depth=depth, weighted=weighted)
         
         if move:
             x, y, jelly = move
             simulated = copy.deepcopy(game_state)
             simulated.make_move(x, y, jelly)
             score = heuristic(simulated, weighted)
 
             if score > best_score:
                 best_score = score
                 best_move = move
 
     return best_move
 
 
def ucs(game_state, max_depth=2):
    open_set = []
    best_move = None
    best_score = float('-inf')
    counter2 = itertools.count()
 
    for y, row in enumerate(game_state.board):
        for x, cell in enumerate(row):
            if cell == ' ':
                for jelly in game_state.playable_jellies:
                    score = game_state.simulate_move(x, y, jelly)
                    if score is not None:
                        cost = -score  # inverso do score = custo (menos pontos → mais custo)
                        heapq.heappush(open_set, (cost, next(counter2), (x, y, jelly), score, 1))
 
    while open_set:
        cost, _, move, total_score, depth = heapq.heappop(open_set)
        x, y, jelly = move
 
        if total_score > best_score:
            best_score = total_score
            best_move = move
 
        if depth < max_depth:
            for y2, row in enumerate(game_state.board):
                for x2, cell in enumerate(row):
                    if cell == ' ':
                        for next_jelly in game_state.playable_jellies:
                            score = game_state.simulate_move(x2, y2, next_jelly)
                            if score is not None:
                                new_cost = cost - score
                                new_score = total_score + score
                                heapq.heappush(open_set, (new_cost, next(counter2), (x2, y2, next_jelly), new_score, depth + 1))
 
    return best_move