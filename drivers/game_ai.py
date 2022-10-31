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
      _, is_changed = self.game.make_move(direction)
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


class MarkovPolicyWithHeuristics(Policy):
  def __init__(self):
    super().__init__()

  def best_move(self):
    best_move, _ = self.best_move_recursive(self.game.board, 3, 1.0)
    return best_move

  def evaluate_move(self, direction):
    pass

  def evaluate_board(self, board=None):
    if board is None:
      board = self.game.board

    steady_increment_score = sum(self.evaluate_steady_increment(board))
    empty_cells_score = self.evaluate_number_of_empty_cells(board)
    proximity_score = self.evaluate_proximity(board)
    
    return steady_increment_score * 3 - (16 - empty_cells_score) ** 2 + proximity_score

  def evaluate_number_of_empty_cells(self, board):
    return np.sum(board == 0)

  def evaluate_steady_increment(self, board):
    updown = leftright = 0

    for row in range(CELL_COUNT):
      left = right = 0
      conseq1 = conseq2 = 0
      
      for col in range(CELL_COUNT - 1):
        if board[row, col] > board[row, col + 1]:
          right += board[row, col]
          conseq1 += 1
          conseq2 = 0
          left -= conseq1 ** 2 * 3
        elif board[row, col] < board[row, col + 1]:
          left += board[row, col + 1]
          conseq1 = 0
          conseq2 += 1
          right -= conseq2 ** 2 * 3
        else:
          conseq1 += 1
          conseq2 += 1
          left -= conseq1 ** 2 * 3
          right -= conseq2 ** 2 * 3
          pass
      leftright -= min(left, right)
      
    for col in range(CELL_COUNT):
      up = down = 0
      conseq1 = conseq2 = 0
      
      for row in range(CELL_COUNT - 1):
        if board[row, col] < board[row + 1, col]:
          up += board[row + 1, col]
          conseq1 += 1
          conseq2 = 0
          down -= (conseq1) ** 2 * 3
        elif board[row, col] > board[row + 1, col]:
          down += board[row, col]
          conseq1 = 0
          conseq2 += 1
          up -= (conseq2) ** 2 * 3
        else:
          conseq1 += 1
          conseq2 += 1
          up -= (conseq1) ** 2 * 3
          down -= (conseq2) ** 2 * 3
          pass
      updown -= min(up, down)
    
    return updown, leftright

  def evaluate_proximity(self, board):
    ans = 0

    for row in range(CELL_COUNT):
      for col in range(CELL_COUNT):
        min_prox = np.inf
        if row:
          min_prox = min(abs(board[row, col] - board[row - 1, col]), min_prox)
        if row < CELL_COUNT - 1:
          min_prox = min(abs(board[row, col] - board[row + 1, col]), min_prox)
        if col:
          min_prox = min(abs(board[row, col] - board[row, col - 1]), min_prox)
        if col < CELL_COUNT - 1:
          min_prox = min(abs(board[row, col] - board[row, col + 1]), min_prox)
      ans += min_prox
    
    return -ans

  def best_move_recursive(self, board, n, prob):
    best_score = -np.inf
    best_move = "up"
    
    for direction in MOVES:
      new_board, score, is_changed = board.make_move(direction)
      if not is_changed:
        continue

      score += self.min_of_possible_moves(new_board, n - 1, prob)

      if score > best_score:
        best_score = score
        best_move = direction

    # try:
    return best_move, best_score
    # except Exception as e:
    #   print(e)
    #   print(score)
    #   print(n)
    #   print(prob)
    #   return "up", 0

  def min_of_possible_moves(self, board, n, prob):
    if n == 0:
      return self.evaluate_board(board)

    scores = []
    zeros = self.evaluate_number_of_empty_cells(board)

    for i in range(4):
      for j in range(4):
        if board[i, j]:
          continue

        score = 0

        for dice, ratio in zip([2, 4], [0.9, 0.1]):
          if ratio * prob < 0.1 and zeros > 5:
            continue

          new_board = board.copy()
          new_board[i, j] = dice
          score += self.best_move_recursive(new_board, n , prob * ratio)[1] * ratio
        
        scores.append(score)
    
    return sum(scores) / len(scores)

  def teardown(self):
    pass
