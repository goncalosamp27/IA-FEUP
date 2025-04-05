def store_test_results(algorithm_name, duration, states_generated, memory_used, moves, results_file="test_results.txt"):
    with open(results_file, 'a') as f:
        f.write(f"Algorithm: {algorithm_name}\n")
        f.write(f"Time: {duration}s\n")
        f.write(f"States Generated: {states_generated}\n")
        f.write(f"Memory Used: {memory_used}MB\n")
        f.write(f"Moves: {moves}\n")
        f.write("=" * 40 + "\n")
