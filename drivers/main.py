from .game import Game
from .game_ai import MonteCarloPolicy

if __name__ == '__main__':
    # game = Game()
    # game.run()

    policy = MonteCarloPolicy()
    policy.run()