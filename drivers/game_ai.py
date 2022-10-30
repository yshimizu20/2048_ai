from constants import *
from game import Game
from board import Board

class Policy():
  def __init__(self):
    self.game = Game()
    self.moves = 0

  def run(self):
    while True:
      self.moves += 1
      self.teardown()
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

  def teardown(self):
    raise NotImplementedError


class RandomPolicy(Policy):
  def __init__(self):
    super().__init__()

  def best_move(self):
    score, is_changed, direction = self.game.random_play()
    return direction

  def evaluate_move(self, direction):
    return 0

  def evaluate_board(self):
    return 0

  def teardown(self):
    pass


class MonteCarloPolicy(Policy):
  def __init__(self):
    super().__init__()

    self.searches_per_move = 200
    self.search_length = 15

  def best_move(self):
    scores = np.zeros(POSSIBLE_MOVES_COUNT)

    for direction in MOVES:
      board, score, is_changed = self.game.board.make_move(direction)
      if not is_changed:
        continue

      board.add_new_tile()
      scores[MOVES.index(direction)] += score
      
      for _ in range(self.searches_per_move):
        move_iter = 1
        game_is_valid = True
        new_board = board.copy()

        while game_is_valid and move_iter < self.search_length:
          new_board, score, game_is_valid = new_board.random_play()
          if not game_is_valid:
            break
          if not new_board.add_new_tile():
            break
          scores[MOVES.index(direction)] += score
          move_iter += 1
      
    best_move = MOVES[np.argmax(scores)]

    return best_move

  def evaluate_board(self):
    pass

  def teardown(self):
    pass


