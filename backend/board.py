import numpy as np
from constants import *
import random

class Board(np.ndarray):
  def __new__(cls, input_array=None):
    if input_array is None:
      obj = np.zeros((CELL_COUNT, CELL_COUNT), dtype=int).view(cls)
    else:
      obj = np.asarray(input_array).view(cls)
    
    return obj

  def __array_finalize__(self, obj):
    if obj is None: return

  def __str__(self):
    return str(self.view(np.ndarray))

  def __repr__(self):
    return repr(self.view(np.ndarray))

  def push_right(self):
    new_board = Board()
    is_changed = False

    for row in range(CELL_COUNT):
      idx = CELL_COUNT - 1
      for col in range(CELL_COUNT - 1, -1, -1):
        if self[row, col] != 0:
          new_board[row, idx] = self[row, col]
          if col != idx:
            is_changed = True
          idx -= 1

    return new_board, is_changed

  def merge_right(self):
    score = 0
    is_changed = False

    for row in range(CELL_COUNT):
      for col in range(CELL_COUNT - 1, 0, -1):
        if self[row, col] == self[row, col - 1] and self[row, col] != 0:
          self[row, col] *= 2
          self[row, col - 1] = 0
          score += self[row, col]
          is_changed = True

    return score, is_changed

  def right_move(self):
    new_board, is_changed = self.push_right()
    score, is_changed2 = new_board.merge_right()
    is_changed = is_changed or is_changed2
    if is_changed:
      new_board, _ = new_board.push_right()

    return new_board, score, is_changed

  def make_move(self, direction):
    if direction == "right":
      new_board, score, is_changed = self.right_move()
    elif direction == "down":
      new_board = np.rot90(self)
      new_board, score, is_changed = new_board.right_move()
      new_board = np.rot90(new_board, -1)
    elif direction == "left":
      new_board = np.rot90(self, 2)
      new_board, score, is_changed = new_board.right_move()
      new_board = np.rot90(new_board, 2)
    elif direction == "up":
      new_board = np.rot90(self, -1)
      new_board, score, is_changed = new_board.right_move()
      new_board = np.rot90(new_board)
    else:
      raise ValueError("Invalid direction")
    
    return new_board, score, is_changed

  def add_new_tile(self):
    empty_cells = np.argwhere(self == 0)
    if len(empty_cells) == 0:
      return False
    
    idx = np.random.randint(len(empty_cells))
    row, col = empty_cells[idx]
    self[row, col] = 2 if np.random.random() < 0.9 else 4

    return True

  def random_play(self):
    move_priority = [0, 1, 2, 3]
    random.shuffle(move_priority)

    while len(move_priority):
      move_index = move_priority.pop()
      new_board, score, is_changed = self.make_move(MOVES[move_index])
      if is_changed:
        return new_board, score, True
    
    return self, 0, False
  
  def __copy__(self):
    return Board(self)