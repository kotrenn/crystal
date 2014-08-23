import pygame
import random

from squaregrid import *
from vector import *

class World(object):
    def __init__(self):
        self.dims = vector(12, 17)
        self.tiles = {
            'blank': [0, 8],
            'tree': [0, 9]
        }
        self.tiles = {k: vector(v) for (k, v) in self.tiles.iteritems()}
        self.grid = SquareGrid(self.dims)

        for row in range(self.dims[0]):
            for col in range(self.dims[1]):
                if random.randint(1, 10) == 1:
                    self.grid.cells[row][col] = self.tiles['tree']
                else:
                    self.grid.cells[row][col] = self.tiles['blank']

    def is_blocked(self, loc):
        if self.grid.out_of_bounds(loc):
            return True
        row = loc[0]
        col = loc[1]
        walls = ['tree']
        tile = self.grid.cells[row][col]
        for wall in walls:
            if self.tiles[wall] == tile:
                return True
        return False
