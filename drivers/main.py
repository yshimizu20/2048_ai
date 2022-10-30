from game_ai import *

if __name__ == '__main__':
    # game = Game()
    # game.run()

    policy = MonteCarloPolicyWithHeuristics()
    policy.run()