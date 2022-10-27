import numpy as np

POSSIBLE_MOVES_COUNT = 4
MOVES = ["up", "right", "left", "down"]
CELL_COUNT = 4
NEW_TILE_DISTRIBUTION = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY = "'d'"
AI_PLAY_KEY = "'p'"

WIN_VALUE = 2048