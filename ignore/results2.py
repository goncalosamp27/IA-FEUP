import csv
import time

def test_algorithm(game_state, algorithm):
    start_time = time.time()

    # Simule o algoritmo com base no estado do jogo
    result = algorithm(game_state)

    end_time = time.time()

    # Coleta de dados
    time_taken = end_time - start_time
    # Adapte para coletar dados específicos como estados gerados, uso de memória, etc.
    states_generated = result['states_generated']  
    memory_usage = result['memory_usage']  
    solution_quality = result['solution_quality']  

    # Salvar os dados no arquivo CSV
    with open('algorithms_comparison.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([algorithm.__name__, time_taken, states_generated, memory_usage, solution_quality])

    return result
