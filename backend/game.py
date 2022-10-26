from constants import *

class Game:
  def __init__(self, win=WIN_VALUE):
    self.win = win
    self.board = np.zeros((CELL_COUNT, CELL_COUNT), dtype=int)
    self.add_new_tile()

  def run(self):
    while True:
      if self.check_win():
        print("You win!")
        return
      
      if not self.add_new_tile():
        print("Game over")
        return

      print(self.board)
      direction = input("")
      self.make_move(direction)

  def add_new_tile(self, n=1):
    for _ in range(n):
      row_options, col_options = np.nonzero(np.logical_not(self.board))
      if len(row_options) == 0:
        return False

      idx = np.random.randint(0, len(row_options))
      self.board[row_options[idx], col_options[idx]] = self.tile_init()

    return True

  def tile_init(self):
    return np.random.choice(NEW_TILE_DISTRIBUTION)

  def check_win(self):
    return self.win in self.board

  def push_right(self):
    new_board = np.zeros((CELL_COUNT, CELL_COUNT), dtype=int)
    is_changed = False

    for row in range(CELL_COUNT):
      idx = CELL_COUNT - 1
      for col in range(CELL_COUNT - 1, -1, -1):
        if self.board[row, col] != 0:
          new_board[row, idx] = self.board[row, col]
          if col != idx:
            is_changed = True
          idx -= 1
    
    self.board = new_board
    return is_changed

  def merge_right(self):
    is_changed = False

    for row in range(CELL_COUNT):
      for col in range(CELL_COUNT - 1, 0, -1):
        if self.board[row, col] == self.board[row, col - 1] and self.board[row, col] != 0:
          self.board[row, col] *= 2
          self.board[row, col - 1] = 0
          is_changed = True

    return is_changed

  def right_move(self):
    is_changed = self.push_right()
    is_changed = self.merge_right() or is_changed
    if is_changed:
      self.push_right()
    
    return is_changed

  def make_move(self, direction):
    if direction == "right":
      is_changed = self.right_move()
    elif direction == "up":
      self.board = np.rot90(self.board, -1)
      is_changed = self.right_move()
      self.board = np.rot90(self.board)
    elif direction == "left":
      self.board = np.rot90(self.board, 2)
      is_changed = self.right_move()
      self.board = np.rot90(self.board, 2)
    elif direction == "down":
      self.board = np.rot90(self.board)
      is_changed = self.right_move()
      self.board = np.rot90(self.board, -1)
    else:
      raise ValueError("Invalid direction")
    
    return is_changed

