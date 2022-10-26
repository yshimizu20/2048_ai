from constants import *
from board import Board
import random

class Game:
  def __init__(self, win=WIN_VALUE):
    self.win = win
    self.board = Board()
    self.add_new_tile()

  def run(self):
    is_changed = True

    while True:
      if self.check_win():
        print("You win!")
        return
      
      if is_changed and not self.add_new_tile():
        print("Game over")
        return

      print(self.board)
      direction = input("")
      new_board, score, is_changed = self.make_move(direction)
      if is_changed:
        self.board = new_board

  def add_new_tile(self):
    return self.board.add_new_tile()

  def check_win(self):
    return self.win in self.board

  def make_move(self, direction):
    return self.board.make_move(direction)

  def random_play(self):
    move_priority = random.shuffle([0, 1, 2, 3])

    while len(move_priority):
      move_index = move_priority.pop()
      score, is_changed = self.make_move(MOVES[move_index])
      if is_changed:
        return score, True
    
    return 0, False
