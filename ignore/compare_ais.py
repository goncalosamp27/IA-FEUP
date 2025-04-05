import pygame, sys
from button import Button
from utils import get_font, SCREEN, BG, CLICK_SOUND

# Função que é chamada ao clicar no botão "Comparar AIs"
def compare_ais_button_click():
    algorithms = ["Greedy", "DFS", "BFS", "A*", "Iterative"]
    
    for algorithm_name in algorithms:
        game_state = GameState(level_file="level.txt", difficulty="medium", disable_randomization=True)

        # Testar o algoritmo
        algorithm = get_algorithm_by_name(algorithm_name)
        result = test_algorithm(game_state, algorithm)

        # Exibir resultados (estatísticas)
        display_results(result)

        # Esperar pela interação do usuário para avançar para o próximo algoritmo
        wait_for_user_input()

# Mapeia o nome do algoritmo para a função correspondente
def get_algorithm_by_name(name):
    algorithms = {
        "Greedy": greedy_algorithm,
        "DFS": dfs_algorithm,
        "BFS": bfs_algorithm,
        "A*": a_star_algorithm,
        "Iterative": iterative_algorithm,
    }
    return algorithms.get(name)

# Exibe os resultados do algoritmo na tela
def display_results(result):
    """
    Exibe as estatísticas do desempenho do algoritmo na tela.
    """
    # Limpa a tela
    SCREEN.fill((0, 0, 0))
    font = get_font(36)
    
    # Renderiza os textos com as estatísticas
    time_text = font.render(f"Time: {result['time_taken']}s", True, (255, 255, 255))
    states_text = font.render(f"States Generated: {result['states_generated']}", True, (255, 255, 255))
    mem_text = font.render(f"Memory Usage: {result['memory_usage']}MB", True, (255, 255, 255))
    quality_text = font.render(f"Solution Quality: {result['solution_quality']}", True, (255, 255, 255))
    
    # Posiciona os textos na tela
    SCREEN.blit(time_text, (100, 100))
    SCREEN.blit(states_text, (100, 150))
    SCREEN.blit(mem_text, (100, 200))
    SCREEN.blit(quality_text, (100, 250))
    
    # Cria o botão "Next AI"
    next_button = Button(
        image=None,
        pos=(640, 500),
        text_input="Next AI",
        font=get_font(36),
        base_color="White",
        hovering_color="Yellow"
    )

    # Espera pela interação do usuário
    waiting = True
    while waiting:
        # Atualiza a tela
        SCREEN.blit(BG, (0, 0))  # Opcional: desenhar o fundo
        SCREEN.blit(time_text, (100, 100))
        SCREEN.blit(states_text, (100, 150))
        SCREEN.blit(mem_text, (100, 200))
        SCREEN.blit(quality_text, (100, 250))
        
        next_button.changeColor(pygame.mouse.get_pos())
        next_button.update(SCREEN)
        pygame.display.update()
        
        # Espera pelo clique do usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.checkForInput(pygame.mouse.get_pos()):
                    CLICK_SOUND.play()
                    waiting = False

# Função para testar o algoritmo
def test_algorithm(game_state, algorithm):
    """
    Executa o algoritmo no estado do jogo e retorna um dicionário com as estatísticas.
    """
    start_time = pygame.time.get_ticks()
    result = algorithm(game_state)  # Aqui o algoritmo precisa retornar um dicionário com as estatísticas
    end_time = pygame.time.get_ticks()
    
    result['time_taken'] = (end_time - start_time) / 1000.0  # Converte para segundos
    return result

# Função que aguarda o clique do usuário para avançar para o próximo algoritmo
def wait_for_user_input():
    """
    Espera pela interação do usuário (clicar para continuar).
    """
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def greedy_algorithm(game_state):
    return {'states_generated': 1000, 'memory_usage': 45, 'solution_quality': 95}

def dfs_algorithm(game_state):
    return {'states_generated': 1500, 'memory_usage': 50, 'solution_quality': 90}

def bfs_algorithm(game_state):
    return {'states_generated': 2000, 'memory_usage': 55, 'solution_quality': 85}

def a_star_algorithm(game_state):
    return {'states_generated': 1200, 'memory_usage': 48, 'solution_quality': 98}

def iterative_algorithm(game_state):
    return {'states_generated': 1800, 'memory_usage': 53, 'solution_quality': 92}
