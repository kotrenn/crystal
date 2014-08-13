import math
import pygame

from vector import *

DIR_NW = 0
DIR_NE = 1
DIR_E = 2
DIR_SE = 3
DIR_SW = 4
DIR_W = 5
NUM_DIRS = 6

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
            DIR_NW: [-1, -1],
            DIR_NE: [-1, 0],
            DIR_E: [0, 1],
            DIR_SE: [1, 1],
            DIR_SW: [1, 0],
            DIR_W: [0, -1]
            }
        lower = {
            DIR_NW: [-1, 0],
            DIR_NE: [-1, 1],
            DIR_E: [0, 1],
            DIR_SE: [1, 0],
            DIR_SW: [1, -1],
            DIR_W: [0, -1]
            }
        middle = {
            DIR_NW: [-1, -1],
            DIR_NE: [-1, 0],
            DIR_E: [0, 1],
            DIR_SE: [1, 0],
            DIR_SW: [1, -1],
            DIR_W: [0, -1]
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

class HexGridViewer(object):
    def __init__(self, grid):
        self.grid = grid
        self.cell_w = 50
        self.cell_h = 50
        #self.cell_w = self.cell_h = 100

    def get_center(self, loc):
        row = loc[0]
        col = loc[1]
        empty = abs(self.grid.size - 1 - row)
        empty_x = empty / 2.0
        offset = vector((col + empty_x) * self.cell_w,
                        0.75 * row * self.cell_h)
        offset += 0.5 * vector(self.cell_w, self.cell_h)
        return offset
        
    def display(self, dst):
        dims = vector(self.cell_w, self.cell_h)
        size = self.grid.size
        max_row = 2 * size - 1
        for row in range(max_row):
            empty = abs(size - 1 - row)
            num_cols = max_row - empty
            for col in range(num_cols):
                white = (255, 255, 255)
                self.draw_hex(dst, [row, col], dims, white)

    def draw_hex(self, dst, loc, dims, color):
        row = loc[0]
        col = loc[1]
        points = [(0, -0.5), (0.5, -0.25),
                  (0.5, 0.25), (0, 0.5),
                  (-0.5, 0.25), (-0.5, -0.25)]
        center = self.get_center(loc)
        final = []
        for p in points:
            pos = vector(p)
            point = center + pos % dims
            final.append(point.list())
        pygame.draw.polygon(dst, color, final, 1)
