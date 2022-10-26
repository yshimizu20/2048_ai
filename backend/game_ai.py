from game import Game
from constants import *

class MonteCarloPolicy(Game):
  moves = ["up", "down", "left", "right"]

  def __init__(self):
    super().__init__()

    self.search_per_move = 20
    self.search_depth = 5
    self.search_param = 200

  def best_move(self):
    pass
  
  def evaluate_board(self):
    pass