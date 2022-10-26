from constants import *
from game import Game
from board import Board

class Policy():
  def __init__(self):
    self.game = Game()

  def run(self):
    while True:
      print(self.game.board)
      direction = self.best_move()
      score, is_changed = self.game.make_move(direction)
      if not is_changed:
        print("Game over")
        return
      is_changed = self.game.add_new_tile()
      if not is_changed:
        print("Game over")
        return

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
    scores = np.zeros(POSSIBLE_MOVES_COUNT)

    for direction in MOVES:
      board, score, is_changed = self.game.board.make_move(direction)
      if not is_changed:
        continue

      board.add_new_tile()
      new_board = board
      scores[MOVES.index(direction)] += score
      
      for _ in range(self.search_per_move):
        move_iter = 1
        game_is_valid = True

        while game_is_valid and move_iter < self.search_depth:
          new_board, score, is_changed = new_board.random_play()
          scores[MOVES.index(direction)] += score
          move_iter += 1
      
    best_move = MOVES[np.argmax(scores)]

    return best_move

  def evaluate_board(self):
    pass