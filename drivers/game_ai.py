from re import L
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

    self.searches_per_move = 300
    self.search_length = 3

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
          # new_board, score, game_is_valid, _ = new_board.random_play()
          if not game_is_valid:
            break
          if not new_board.add_new_tile():
            break
          scores[MOVES.index(direction)] += score
          move_iter += 1
      
    best_move = MOVES[np.argmax(scores)]

    return best_move

  def evaluate_board(self):
    return 0

  def teardown(self):
    pass


class MonteCarloPolicyWithHeuristics(Policy):
  def __init__(self):
    super().__init__()

    # self.searches_per_move = 200
    # self.search_length = 10

  def best_move(self):
    # scores = np.zeros(POSSIBLE_MOVES_COUNT)

    # for direction in MOVES:
    #   board, score, is_changed = self.game.board.make_move(direction)
    #   if not is_changed:
    #     scores[MOVES.index(direction)] = -np.inf
    #     continue

    #   board.add_new_tile()
    #   scores[MOVES.index(direction)] += self.evaluate_board(board) * 200
    #   scores[MOVES.index(direction)] += score
      
    #   for _ in range(self.searches_per_move):
    #     move_iter = 1
    #     game_is_valid = True
    #     new_board = board.copy()

    #     while game_is_valid and move_iter < self.search_length:
    #       new_board, score, game_is_valid, _ = new_board.random_play()

    #       if not game_is_valid:
    #         break
    #       if not new_board.add_new_tile():
    #         break
    #       scores[MOVES.index(direction)] += score
    #       move_iter += 1
      
    # best_move = MOVES[np.argmax(scores)]

    # return best_move

    best_move, _ = self.best_move_recursive(self.game.board, 4)
    return best_move

  def evaluate_move(self, direction):
    pass

  def evaluate_board(self, board=None):
    if board is None:
      board = self.game.board

    steady_increment_score = sum(self.evaluate_steady_increment(board))
    empty_cells_score = self.evaluate_number_of_empty_cells(board)
    proximity_score = self.evaluate_proximity(board)
    return steady_increment_score + empty_cells_score ** 2 + proximity_score * 10

  def evaluate_number_of_empty_cells(self, board):
    return np.sum(board == 0)

  def evaluate_steady_increment(self, board):
    up = down = left = right = 0

    for row in range(CELL_COUNT):
      for col in range(CELL_COUNT - 1):
        if board[row, col] > board[row, col + 1]:
          right += board[row, col]
        if board[col, row] < board[col + 1, row]:
          down += board[col + 1, row]
      
    for col in range(CELL_COUNT):
      for row in range(CELL_COUNT - 1):
        if board[row, col] < board[row + 1, col]:
          up += board[row + 1, col]
        if board[row, col] > board[row + 1, col]:
          left += board[row, col]
    
    return -min(up, down), -min(left, right)

  def evaluate_proximity(self, board):
    ans = 0

    for row in range(CELL_COUNT):
      for col in range(CELL_COUNT):
        min_prox = np.inf
        if row:
          min_prox = min(board[row, col], min_prox)
        if row < CELL_COUNT - 1:
          min_prox = min(board[row, col], min_prox)
        if col:
          min_prox = min(board[row, col], min_prox)
        if col < CELL_COUNT - 1:
          min_prox = min(board[row, col], min_prox)
      ans += min_prox
    
    return -ans

  def best_move_recursive(self, board, n):
    if n == 0:
      return None, 0

    scores = np.zeros(POSSIBLE_MOVES_COUNT)

    for direction in MOVES:
      new_board, score, is_changed = board.make_move(direction)
      if not is_changed:
        scores[MOVES.index(direction)] = -np.inf
        continue

      scores[MOVES.index(direction)] += score
      scores[MOVES.index(direction)] += self.evaluate_board(new_board)
      if not new_board.add_new_tile():
        continue
      scores[MOVES.index(direction)] += self.best_move_recursive(new_board, n-1)[1]
      
    best_move = MOVES[np.argmax(scores)]

    return best_move, np.max(scores)

  def teardown(self):
    pass
