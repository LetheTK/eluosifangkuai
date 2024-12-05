import random
from tetris.constants import COLORS, GRID_WIDTH

class Tetromino:
    SHAPES = {
        'I': [[0, 0, 0, 0],
              [1, 1, 1, 1],
              [0, 0, 0, 0],
              [0, 0, 0, 0]],
        'O': [[1, 1],
              [1, 1]],
        'T': [[0, 1, 0],
              [1, 1, 1],
              [0, 0, 0]],
        'L': [[0, 0, 1],
              [1, 1, 1],
              [0, 0, 0]],
        'J': [[1, 0, 0],
              [1, 1, 1],
              [0, 0, 0]],
        'S': [[0, 1, 1],
              [1, 1, 0],
              [0, 0, 0]],
        'Z': [[1, 1, 0],
              [0, 1, 1],
              [0, 0, 0]]
    }

    def __init__(self):
        self.shape_name = random.choice(list(self.SHAPES.keys()))
        self.shape = [row[:] for row in self.SHAPES[self.shape_name]]
        self.color = COLORS[self.shape_name]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows-1-r] = self.shape[r][c]
        self.shape = rotated
  