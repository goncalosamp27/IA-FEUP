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