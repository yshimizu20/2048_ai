from constants import *
from game import Game

class Policy():
  def __init__(self):
    self.game = Game()

  def best_move(self):
    raise NotImplementedError

  def evaluate_move(self, direction):
    raise NotImplementedError

  def evaluate_board(self):
    raise NotImplementedError


class MonteCarloPolicy(Policy):
  def __init__(self):
    super().__init__()

    self.search_per_move = 20
    self.search_depth = 5
    self.search_param = 200

  def best_move(self):
    pass

  def evaluate_board(self):
    pass