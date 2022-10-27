import tkinter as tk
from drivers.game import Game
from gui_util.constants import *

class Display(tk.Frame):
  def __init__(self):
    tk.Frame.__init__(self)

    self.game = Game()

    self.grid()
    self.master.title("2048 game")
    # self.master.bind("<Key>", self.key_pressed)

    self.grid_cells = []
    self.init_grid()
    self.update_grid_cells()

    # self.commands = {
    #   UP_KEY: self.up_key,
    #   DOWN_KEY: self.down_key,
    #   LEFT_KEY: self.left_key,
    #   RIGHT_KEY: self.right_key,
    # }

    self.master.bind("<Up>", self.up_key)
    self.master.bind("<Down>", self.down_key)
    self.master.bind("<Left>", self.left_key)
    self.master.bind("<Right>", self.right_key)

  # def key_pressed(self, event):
  #   key = repr(event.char)

  #   if key not in self.commands:
  #     print("Invalid key")
  #     return

  #   _, is_valid = self.game.make_move(self.commands[key])
  #   if is_valid:
  #     self.game.add_new_tile()
  #     self.update_grid_cells()
  #   else:
  #     print("Invalid move")

  def init_grid(self):
    background = tk.Frame(self, bg=BACKGROUND_COLOR_GAME, width=EDGE_LENGTH, height=EDGE_LENGTH)
    background.grid()

    for i in range(CELL_COUNT):
      grid_row = []
      for j in range(CELL_COUNT):
        cell = tk.Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=EDGE_LENGTH / CELL_COUNT, height=EDGE_LENGTH / CELL_COUNT)
        cell.grid(row=i, column=j, padx=CELL_PADDING, pady=CELL_PADDING)
        t = tk.Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=tk.CENTER, font=FONT, width=5, height=2)
        t.grid()
        grid_row.append(t)

      self.grid_cells.append(grid_row)

  def update_grid_cells(self):
    for row in range(CELL_COUNT):
      for col in range(CELL_COUNT):
        val = self.game.board[row][col]
        if val == 0:
          self.grid_cells[row][col].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
        else:
          self.grid_cells[row][col].configure(text=str(val), bg=BACKGROUND_COLOR_DICT[val], fg=CELL_COLOR_DICT[val])

  def left_key(self, event):
    _, is_valid = self.game.make_move("left")
    if is_valid:
      self.game.add_new_tile()
      self.update_grid_cells()
    else:
      print("Invalid move")
  
  def right_key(self, event):
    _, is_valid = self.game.make_move("right")
    if is_valid:
      self.game.add_new_tile()
      self.update_grid_cells()
    else:
      print("Invalid move")

  def up_key(self, event):
    _, is_valid = self.game.make_move("up")
    if is_valid:
      self.game.add_new_tile()
      self.update_grid_cells()
    else:
      print("Invalid move")
  
  def down_key(self, event):
    _, is_valid = self.game.make_move("down")
    if is_valid:
      self.game.add_new_tile()
      self.update_grid_cells()
    else:
      print("Invalid move")


if __name__ == "__main__":
  game = Display()
  game.mainloop()