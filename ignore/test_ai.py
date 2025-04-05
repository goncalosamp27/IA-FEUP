

import pygame
import time
# Assuming store_test_results is already defined

def test_mode(config):
    # Set up the initial game state based on the config
    board_size = config['board_size']
    difficulty = config['difficulty']
    algorithms = config['algorithms']
    randomization = config['randomization']
    # Set up your board and game state here

    # Initialize the test results file
    results_file = "test_results.txt"
    
    # Pygame setup (window size, fonts, etc.)
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("AI Test Mode")
    font = pygame.font.Font(None, 36)

    # Loop through each algorithm and test
    for algorithm in algorithms:
        print(f"Testing {algorithm}...")

        # Set up the game for the specific algorithm (ensure the same initial state)
        # (Reset the board, game settings, and any other necessary parts here)
        
        # Start the timer
        start_time = time.time()

        # Simulate the AI's play and track performance
        # Example simulation
        duration = round(time.time() - start_time, 2)
        states_generated = 1000  # Example
        memory_used = 50  # Example (in MB)
        moves = 25  # Example
        
        # Store the results for this algorithm
        store_test_results(algorithm, duration, states_generated, memory_used, moves, results_file)

        # Show the result on the screen
        SCREEN.fill((0, 0, 0))  # Clear screen

        # Render results text
        result_text = font.render(f"Results for {algorithm}", True, (255, 255, 255))
        SCREEN.blit(result_text, (50, 50))

        time_text = font.render(f"Time: {duration}s", True, (255, 255, 255))
        SCREEN.blit(time_text, (50, 100))

        states_text = font.render(f"States Generated: {states_generated}", True, (255, 255, 255))
        SCREEN.blit(states_text, (50, 150))

        memory_text = font.render(f"Memory Used: {memory_used}MB", True, (255, 255, 255))
        SCREEN.blit(memory_text, (50, 200))

        moves_text = font.render(f"Moves: {moves}", True, (255, 255, 255))
        SCREEN.blit(moves_text, (50, 250))

        # Create "Next" button
        next_button = pygame.Rect(540, 300, 200, 50)
        pygame.draw.rect(SCREEN, (0, 255, 0), next_button)
        next_button_text = font.render("Next AI", True, (0, 0, 0))
        SCREEN.blit(next_button_text, (next_button.centerx - next_button_text.get_width() // 2, next_button.centery - next_button_text.get_height() // 2))

        # Refresh the screen
        pygame.display.flip()

        # Wait for the user to click the "Next" button
        waiting_for_next = True
        while waiting_for_next:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_button.collidepoint(event.pos):
                        waiting_for_next = False

    pygame.quit()  # Quit Pygame when done

