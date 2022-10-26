from constants import *
from board import Board

class Game:
  def __init__(self, win=WIN_VALUE):
    self.win = win
    self.board = Board()
    self.add_new_tile(2)

  def run(self):
    is_changed = True

    while True:
      if self.check_win():
        print("You win!")
        return

      print(self.board)
      direction = input("")
      new_board, score, is_changed = self.make_move(direction)
      if is_changed:
        self.board = new_board
        if not self.add_new_tile():
          print("Game over")
          return

  def add_new_tile(self, n=1):
    for _ in range(n-1):
      self.board.add_new_tile()

    return self.board.add_new_tile()

  def check_win(self):
    return self.win in self.board

  def make_move(self, direction):
    new_board, score, is_changed = self.board.make_move(direction)
    self.board = new_board

    return score, is_changed

  def random_play(self):
    new_board, score, is_changed = self.board.random_play()
    self.board = new_board

    return score, is_changed
