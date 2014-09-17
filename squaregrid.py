import pygame

from vector import *

DIR_NONE = -1
DIR_NW = 0
DIR_N = 1
DIR_NE = 2
DIR_E = 3
DIR_SE = 4
DIR_S = 5
DIR_SW = 6
DIR_W = 7

class SquareGrid(object):
    dir_mapping = {
            DIR_NONE: [0, 0],
            DIR_NW: [-1, -1],
            DIR_N: [-1, 0],
            DIR_NE: [-1, 1],
            DIR_E: [0, 1],
            DIR_SE: [1, 1],
            DIR_S: [1, 0],
            DIR_SW: [1, -1],
            DIR_W: [0, -1]
        }
    
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
        return vector(SquareGrid.dir_mapping[dir])

    def move_loc(self, dir, loc):
        return loc + self.dir_vel(dir)

    def out_of_bounds(self, loc):
        row, col = loc.list()
        return row < 0 or col < 0 or \
            row >= self.num_rows() or \
            col >= self.num_cols()

    def best_dir(self, loc, dst):
        dx, dy = (dst - loc).tuple()
        if dx < 0:
            if dy < 0:
                return DIR_SW
            elif dy > 0:
                return DIR_NW
            else:
                return DIR_W
        elif dx > 0:
            if dy < 0:
                return DIR_SE
            elif dy > 0:
                return DIR_NE
            else:
                return DIR_E
        elif dy < 0:
            return DIR_S
        elif dy > 0:
            return DIR_N
        else:
            return DIR_NONE
