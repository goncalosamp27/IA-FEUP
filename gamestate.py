import random, pygame, copy
from jelly import Jelly
from utils import COLORS, POP_SOUND, TILE_TEXTURE, HINT_TEXTURE
from itertools import cycle

class GameState:
    COLORS = COLORS

    def __init__(self, level_file, difficulty, is_test=True):
        self.board = self.load_board(level_file)
        self.difficulty = difficulty
        self.objective = self.generate_objective()
        
        if is_test:
            print("Tabuleiro de teste carregado.")
            self.set_fixed_jellies_positions()
            self.generate_fixed_playable_jellies()
        else:
            self.randomize_jellies()
            self.generate_playable_jellies() 
            
        #self.randomize_jellies()
        #self.generate_playable_jellies() 
        self.selected_jelly = None
        self.scheduled_actions = []
        
    #def set_fixed_jellies_positions(self):
    
    def set_fixed_jellies_positions(self):
        jelly1 = Jelly(0, 0, "#e08b8b", "#7fc57b", "#e0c750", "#9a64c0")  # Vermelho, Verde, Amarelo, Roxo
        jelly2 = Jelly(0, 0, "#5fb5ae", "#5b97c2", "#e08b8b", "#7fc57b")  # Ciano, Azul, Vermelho, Verde
        jelly3 = Jelly(0, 0, "#9a64c0", "#e08b8b", "#7fc57b", "#e0c750")  # Roxo, Vermelho, Verde, Amarelo
        jelly4 = Jelly(0, 0, "#5fb5ae", "#9a64c0", "#7fc57b", "#e0c750")  # Ciano, Roxo, Verde, Amarelo
        jelly5 = Jelly(0, 0, "#7fc57b", "#5b97c2", "#e08b8b", "#9a64c0")  # Verde, Azul, Vermelho, Roxo

        self.fixed_jellies = [jelly1, jelly2, jelly3, jelly4, jelly5]

        self.fixed_jelly_cycle = cycle(self.fixed_jellies)

        # Atribuir as jellies à posição no tabuleiro
        for y, row in enumerate(self.board):
            for x in range(len(row)):
                if row[x] == 'X':  # Se for uma célula jogável
                    jelly = next(self.fixed_jelly_cycle)
                    self.board[y][x] = jelly
                else:
                    row[x] = ' '  # Deixa as células não jogáveis vazias

    def generate_fixed_playable_jellies(self):
        # Gerando a lista de 50 jellies usando o ciclo das 5 jellies fixas
        self.playable_jellies = []

        # Criando uma lista de 50 jellies a partir das 5 fixas
        for _ in range(50):
            jelly = next(self.fixed_jelly_cycle)
            self.playable_jellies.append(jelly)
        
        # Usando itertools.cycle para garantir que a sequência de 5 jellies seja cíclica
        self.playable_jelly_cycle = cycle(self.playable_jellies)

    def load_board(self, level_file):
        with open(level_file, 'r') as file:
            board = [list(line.strip()) for line in file.readlines()]
        return board

    def randomize_jellies(self):
        if self.difficulty == 'easy':
            fill_percent = 0.2
        elif self.difficulty == 'medium':
            fill_percent = 0.4
        else:  # hard
            fill_percent = 0.6

        available_positions = []

        for y, row in enumerate(self.board):
            for x in range(len(row)):
                if row[x] == 'X':
                    available_positions.append((x, y))

        total_playable = len(available_positions)
        num_jellies = max(1, int(total_playable * fill_percent))  

        random.shuffle(available_positions)
        chosen = set(available_positions[:num_jellies])


        for y, row in enumerate(self.board):
            for x in range(len(row)):
                if (x, y) in chosen:
                    jelly = Jelly(0, 0, None, None, None, None)
                    self.set_unique_random_colors(jelly, y, x)
                    row[x] = jelly
                elif row[x] == 'X':
                    row[x] = ' '  


    def set_unique_random_colors(self, jelly, y, x):
        adjacent_colors = set()
        if y > 0 and isinstance(self.board[y-1][x], Jelly):
            adjacent_colors.update(self.board[y-1][x].get_colors())
        if x > 0 and isinstance(self.board[y][x-1], Jelly):
            adjacent_colors.update(self.board[y][x-1].get_colors())

        available_colors = [color for color in Jelly.COLORS if color not in adjacent_colors]

        if not available_colors:
            available_colors = self.COLORS  # fallback

        jelly.tl = random.choice(available_colors)
        jelly.tr = random.choice(available_colors)
        jelly.bl = random.choice(available_colors)
        jelly.br = random.choice(available_colors)

    def generate_playable_jellies(self):
        self.playable_jellies = [self.create_random_jelly(), self.create_random_jelly()]

    def create_random_jelly(self):
        jelly = Jelly(0, 0, None, None, None, None)
        jelly.set_random_colors()
        return jelly

    def generate_objective(self):
        if self.difficulty == 'easy':
            color1 = random.choice(self.COLORS)
            color2 = random.choice(self.COLORS)

            while color2 == color1:
                color2 = random.choice(self.COLORS)

            return {
                "color1": color1,
                "count1": 10,
                "color2": color2,
                "count2": 5
            }

        elif self.difficulty == 'medium':
            color1 = random.choice(self.COLORS)
            color2 = random.choice(self.COLORS)
            color3 = random.choice(self.COLORS)

            while color2 == color1:
                color2 = random.choice(self.COLORS)
            while color3 == color1 or color3 == color2:
                color3 = random.choice(self.COLORS)

            return {
                "color1": color1,
                "count1": 10,
                "color2": color2,
                "count2": 7,
                "color3": color3,
                "count3": 5
            }

        else:  # Difícil
            color1 = random.choice(self.COLORS)
            color2 = random.choice(self.COLORS)
            color3 = random.choice(self.COLORS)

            while color2 == color1:
                color2 = random.choice(self.COLORS)
            while color3 == color1 or color3 == color2:
                color3 = random.choice(self.COLORS)

            return {
                "color1": color1,
                "count1": 15,
                "color2": color2,
                "count2": 10,
                "color3": color3,
                "count3": 7
            }
        
    """ Drawing Functions """
        
    def get_board_offsets(self, screen):
        board_width = len(self.board[0]) * Jelly.SIZE
        board_height = len(self.board) * Jelly.SIZE
        screen_width, screen_height = screen.get_size()
        offset_x = (screen_width - board_width) // 2
        offset_y = (screen_height - board_height) // 2 - 100
        return offset_x, offset_y, board_width, board_height  

    def get_cell_position(self, x, y, offset_x, offset_y):
        return x * Jelly.SIZE + offset_x, y * Jelly.SIZE + offset_y

    def draw_cell(self, screen, cell, draw_x, draw_y, is_hint=False):
        texture = HINT_TEXTURE if is_hint else TILE_TEXTURE
        texture_scaled = pygame.transform.scale(texture, (Jelly.SIZE, Jelly.SIZE))
        screen.blit(texture_scaled, (draw_x, draw_y))

        if isinstance(cell, Jelly):
            cell.set_position(draw_x, draw_y)
            cell.draw(screen)

    def draw_playable_jellies(self, screen, offset_x, offset_y, board_width, board_height, hint_move=None):
        jelly_y = offset_y + board_height + 50
        for i, jelly in enumerate(self.playable_jellies):
            jelly_x = offset_x if i == 0 else offset_x + board_width - Jelly.SIZE
            if hint_move and hint_move[2] == jelly:
                pygame.draw.rect(screen, (255, 255, 0), (jelly_x - 5, jelly_y - 5, Jelly.SIZE + 10, Jelly.SIZE + 10), 5)
            if jelly == self.selected_jelly:
                jelly.set_position(jelly_x - 10, jelly_y - 10)
                jelly.draw(screen, size=Jelly.SIZE + 20)
            else:
                jelly.set_position(jelly_x, jelly_y)
                jelly.draw(screen)

    def draw_objectives(self, screen):
        font = pygame.font.Font("assets/font.ttf", 40)
        y_offset = 20
        for i in range(1, 4):
            color_key = f"color{i}"
            count_key = f"count{i}"
            if color_key in self.objective and count_key in self.objective:
                color_rgb = pygame.Color(self.objective[color_key])
                text_surface = font.render(f"Pop {self.objective[count_key]}", True, color_rgb)
                screen.blit(text_surface, (20, y_offset))
                y_offset += 60

    def draw_board(self, screen, hint_move=None):
        offset_x, offset_y, board_width, board_height = self.get_board_offsets(screen)

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == ' ' or isinstance(cell, Jelly):
                    draw_x, draw_y = self.get_cell_position(x, y, offset_x, offset_y)
                    is_hint = hint_move and hint_move[0] == x and hint_move[1] == y
                    self.draw_cell(screen, cell, draw_x, draw_y, is_hint=is_hint)

        self.draw_playable_jellies(screen, offset_x, offset_y, board_width, board_height, hint_move)
        self.draw_objectives(screen)


    """ Movement Functions """

    def select_jelly(self, jelly):
        self.selected_jelly = None if self.selected_jelly == jelly else jelly

    def make_move(self, x, y, jelly):
        if self.board[y][x] == ' ':  
            self.board[y][x] = jelly
            self.replace_played_jelly(jelly)
            self.selected_jelly = None
            return True
        else:
            return False
        
    def replace_played_jelly(self, played_jelly):
        new_jelly = self.create_random_jelly()
        for i in range(len(self.playable_jellies)):
            if self.playable_jellies[i] == played_jelly:
                self.playable_jellies[i] = new_jelly
                break

    """ Objective and End Game Functions """

    def decrement_objective(self, destroyed_color1, destroyed_color2, destroyed_color3):
        destroyed_colors = [destroyed_color1, destroyed_color2, destroyed_color3]  

        for i in range(3):  
            count_key = f"count{i+1}"

            if count_key in self.objective:
                self.objective[count_key] = max(0, self.objective[count_key] - destroyed_colors[i]) 

    def check_game_over(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    
    def check_game_win(self):
        for i in range(1, 4):
            count_key = f"count{i}"
            if count_key in self.objective and self.objective[count_key] > 0:
                return False
        return True

    """ Normalization Functions """

    def is_board_normalized(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if not isinstance(self.board[y][x], Jelly):
                    continue  

                jelly = self.board[y][x]

                left_jelly = None
                right_jelly = None
                top_jelly = None
                bottom_jelly = None

                if x > 0 and isinstance(self.board[y][x - 1], Jelly):
                    left_jelly = self.board[y][x - 1]
                if x < len(self.board[y]) - 1 and isinstance(self.board[y][x + 1], Jelly):
                    right_jelly = self.board[y][x + 1]
                if y > 0 and isinstance(self.board[y - 1][x], Jelly):
                    top_jelly = self.board[y - 1][x]
                if y < len(self.board) - 1 and isinstance(self.board[y + 1][x], Jelly):
                    bottom_jelly = self.board[y + 1][x]

                if left_jelly and jelly.tl == left_jelly.tr:
                    return False
                if top_jelly and jelly.tl == top_jelly.bl:
                    return False
                if right_jelly and jelly.tr == right_jelly.tl:
                    return False
                if top_jelly and jelly.tr == top_jelly.br:
                    return False
                if left_jelly and jelly.bl == left_jelly.br:
                    return False
                if bottom_jelly and jelly.bl == bottom_jelly.tl:
                    return False
                if right_jelly and jelly.br == right_jelly.bl:
                    return False
                if bottom_jelly and jelly.br == bottom_jelly.tr:
                    return False
        return True
    
    def normalize_board(self):
        to_destroy = self.find_matching_corners()
        to_destroy = self.expand_matches_inside_jellies(to_destroy)
        destroyed_colors = self.destroy_corners(to_destroy)
        self.update_objective_with_destructions(destroyed_colors)

    def find_matching_corners(self):
        to_destroy = set()

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if not isinstance(self.board[y][x], Jelly):
                    continue

                jelly = self.board[y][x]

                def get_jelly(nx, ny):
                    if 0 <= ny < len(self.board) and 0 <= nx < len(self.board[ny]):
                        neighbor = self.board[ny][nx]
                        if isinstance(neighbor, Jelly):
                            return neighbor
                    return None

                directions = [
                    ('tl', -1,  0, 'tr'),
                    ('tl',  0, -1, 'bl'),
                    ('tr',  1,  0, 'tl'),
                    ('tr',  0, -1, 'br'),
                    ('bl', -1,  0, 'br'),
                    ('bl',  0,  1, 'tl'),
                    ('br',  1,  0, 'bl'),
                    ('br',  0,  1, 'tr'),
                ]

                for own_corner, dx, dy, neighbor_corner in directions:
                    neighbor = get_jelly(x + dx, y + dy)
                    if neighbor:
                        own_color = getattr(jelly, own_corner)
                        neighbor_color = getattr(neighbor, neighbor_corner)
                        if own_color is not None and own_color == neighbor_color:
                            to_destroy.add((jelly, own_corner))
                            to_destroy.add((neighbor, neighbor_corner))

        return to_destroy

    def expand_matches_inside_jellies(self, to_destroy):
        expanded = set()

        for jelly, corner in to_destroy:
            expanded |= self.expand_inside_jelly(jelly, corner)

        to_destroy.update(expanded)
        return to_destroy

    def expand_inside_jelly(self, jelly, start_corner):
        visited = set()
        stack = [start_corner]
        color = getattr(jelly, start_corner)

        internal_adjacents = {
            'tl': ['tr', 'bl'],
            'tr': ['tl', 'br'],
            'bl': ['tl', 'br'],
            'br': ['tr', 'bl'],
        }

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            for neighbor in internal_adjacents[current]:
                if getattr(jelly, neighbor) == color:
                    stack.append(neighbor)

        return {(jelly, corner) for corner in visited}

    def destroy_corners(self, to_destroy):
        from collections import Counter
        destroyed_colors = Counter()

        for jelly, corner in to_destroy:
            color = getattr(jelly, corner)
            if color:
                destroyed_colors[color] += 1
            setattr(jelly, corner, None)
            POP_SOUND.play()

        return destroyed_colors

    def update_objective_with_destructions(self, destroyed_colors):
        color1 = self.objective.get("color1")
        color2 = self.objective.get("color2")
        color3 = self.objective.get("color3")

        self.decrement_objective(
            destroyed_colors.get(color1, 0),
            destroyed_colors.get(color2, 0),
            destroyed_colors.get(color3, 0)
        )


    def reconstruct_all(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                jelly = self.board[y][x]
                if isinstance(jelly, Jelly):
                    corners = [jelly.tl, jelly.tr, jelly.bl, jelly.br]

                    if all(c is None for c in corners):
                        self.board[y][x] = ' '  
                    elif any(c is None for c in corners):
                        jelly.reconstruct()  

    def update_scheduled_actions(self):
        now = pygame.time.get_ticks()
        remaining = []

        for exec_time, action in self.scheduled_actions:
            if now >= exec_time:
                action()
            else:
                remaining.append((exec_time, action))

        self.scheduled_actions = remaining

        if not self.scheduled_actions and self.check_game_win():
            print("You won!")
            pygame.time.set_timer(pygame.USEREVENT, 1000)


    def schedule_board_normalization_sequence(self):
        now = pygame.time.get_ticks()
        delay = 250  

        self.scheduled_actions = []  

        self.scheduled_actions.append((now + delay * 1, lambda: print("Not Normalizado")))
        self.scheduled_actions.append((now + delay * 2, self.normalize_board))
        self.scheduled_actions.append((now + delay * 3, self.reconstruct_all))
        
    """ Eval Functions """
    def simulate_move(self, x, y, jelly):
        if self.board[y][x] != ' ':  
            return None 

        simulated_state = copy.deepcopy(self)

        simulated_state.board[y][x] = jelly
        simulated_state.replace_played_jelly(jelly)
        simulated_state.update_scheduled_actions()
        normalization_triggered = False
        freed_cells = 0

        if not simulated_state.is_board_normalized() and not simulated_state.scheduled_actions:
            normalization_triggered = True
            pre_normalization_empty_cells = sum(row.count(' ') for row in simulated_state.board)
            simulated_state.schedule_board_normalization_sequence()
            post_normalization_empty_cells = sum(row.count(' ') for row in simulated_state.board)
            freed_cells = post_normalization_empty_cells - pre_normalization_empty_cells

        score = simulated_state.evaluate_state(normalization_triggered, freed_cells)

        return score
    
    def evaluate_state(self, normalization_triggered=False, freed_cells=0):
        WIN_SCORE = 1_000_000  
        LOSS_SCORE = -1_000_000  
        OBJECTIVE_WEIGHT = 250 
        NORMALIZATION_WEIGHT = 50  
        FREED_CELL_BONUS = 10

        if self.check_game_win():
            return WIN_SCORE
        if self.check_game_over():
            return LOSS_SCORE

        score = 0

        for i in range(1, 4):
            count_key = f"count{i}"
            if count_key in self.objective and self.objective[count_key] > 0:
                initial_target = {
                    "easy": [10, 5],
                    "medium": [10, 7, 5],
                    "hard": [15, 10, 7]
                } [self.difficulty][i - 1]
                progress = initial_target - self.objective[count_key]
                score += progress * OBJECTIVE_WEIGHT

        if normalization_triggered:
            score += NORMALIZATION_WEIGHT
            score += freed_cells * FREED_CELL_BONUS

        return score


