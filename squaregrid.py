import pygame

from vector import *

DIR_NW = 0
DIR_N = 1
DIR_NE = 2
DIR_E = 3
DIR_SE = 4
DIR_S = 5
DIR_SW = 6
DIR_W = 7

class SquareGrid(object):
    def __init__(self, size):
        self.size = size
        self.cells = []
        for row in range(self.num_rows()):
            cur_row = []
            for col in range(self.num_cols()):
                cur_row.append(None)
            self.cells.append(cur_row)

    def num_rows(self):
        return self.size[0]

    def num_cols(self):
        return self.size[1]

    def dir_vel(self, dir):
        mapping = {
            DIR_NW: [-1, -1],
            DIR_N: [-1, 0],
            DIR_NE: [-1, 1],
            DIR_E: [0, 1],
            DIR_SE: [1, 1],
            DIR_S: [1, 0],
            DIR_SW: [1, -1],
            DIR_W: [0, -1]
        }
        ret = mapping[dir]
        return vector(ret)

    def move_loc(self, dir, loc):
        vel = self.dir_vel(dir, loc)
        return loc + vel

    def out_of_bounds(self, loc):
        row, col = loc.list()
        return row < 0 or col < 0 or \
            row >= self.num_rows() or \
            col >= self.num_cols()
