# stats.py
class GameStats:
    def __init__(self):
        self.moves = 0
        self.duration = 0.0  # em segundos
        self.algorithm = "Human"
        self.depth = None  # opcional, para DFS/BFS/etc

    def reset(self):
        self.__init__()

game_stats = GameStats()
