import math
import pygame

from vector import *

HEX_NW = 0
HEX_NE = 1
HEX_E = 2
HEX_SE = 3
HEX_SW = 4
HEX_W = 5
HEX_NUM_DIRS = 6

class HexGrid(object):
    def __init__(self, size):
        self.size = size
        self.cells = []
        for row in range(self.num_rows()):
            cur_row = []
            for col in range(self.num_cols(row)):
                cur_row.append(None)
            self.cells.append(cur_row)

    def num_rows(self):
        return 2 * self.size - 1

    def num_cols(self, row):
        max_row = self.num_rows()
        empty = abs(self.size - 1 - row)
        row_len = max_row - empty
        return row_len

    def dir_vel(self, dir, loc):
        mid = self.size - 1
        upper = {
            HEX_NW: [-1, -1],
            HEX_NE: [-1, 0],
            HEX_E: [0, 1],
            HEX_SE: [1, 1],
            HEX_SW: [1, 0],
            HEX_W: [0, -1]
        }
        lower = {
            HEX_NW: [-1, 0],
            HEX_NE: [-1, 1],
            HEX_E: [0, 1],
            HEX_SE: [1, 0],
            HEX_SW: [1, -1],
            HEX_W: [0, -1]
        }
        middle = {
            HEX_NW: [-1, -1],
            HEX_NE: [-1, 0],
            HEX_E: [0, 1],
            HEX_SE: [1, 0],
            HEX_SW: [1, -1],
            HEX_W: [0, -1]
        }
        if loc[0] < mid:
            ret = upper[dir]
        elif loc[0] > mid:
            ret = lower[dir]
        else:
            ret = middle[dir]
        return vector(ret)

    def move_loc(self, dir, loc):
        vel = self.dir_vel(dir, loc)
        return loc + vel

    def out_of_bounds(self, loc):
        row, col = loc.list()
        return row < 0 or col < 0 or \
            row >= self.num_rows() or \
            col >= self.num_cols(row)
