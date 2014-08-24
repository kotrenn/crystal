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
        ret = mapping[dir]
        return vector(ret)

    def move_loc(self, dir, loc):
        vel = self.dir_vel(dir)
        return loc + vel

    def out_of_bounds(self, loc):
        row, col = loc.list()
        return row < 0 or col < 0 or \
            row >= self.num_rows() or \
            col >= self.num_cols()

    def a_star(self, src, dst):
        # currently just dijkstra's
        dirs = [DIR_NW, DIR_N, DIR_NE, DIR_E,
                DIR_SE, DIR_S, DIR_SW, DIR_W]
        q = [(DIR_NONE, vector(src))]
        ret = []
        done = False
        finished = []
        while len(q) > 0 and not done:
            dir, loc = q.pop(0)
            if loc.list() in finished:
                continue
