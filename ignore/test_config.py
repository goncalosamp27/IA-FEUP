import os

def load_game_config(file_path="game_config.txt"):
    config = {}
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith("#"):  # Skip comments
                    continue
                key, value = line.strip().split("=")
                config[key.strip()] = value.strip()
    else:
        print(f"Config file {file_path} not found. Using default settings.")
        config = {
            'board_size': '5',
            'difficulty': 'medium',
            'randomization': 'false',
            'algorithms': 'greedy, dfs, bfs, a_star',
            'level_file': 'levels/level1.txt'
        }
    
    # Convert the necessary settings to the correct types
    config['board_size'] = int(config['board_size'])
    config['randomization'] = config['randomization'].lower() == 'true'
    config['algorithms'] = config['algorithms'].split(', ')
    
    return config
