import pygame
import random

from squaregrid import *
from squaregridviewer import *
from vector import *
from window import *

class WorldViewer(Window):
    def __init__(self, parent, player):
        Window.__init__(self, parent)
        self.dims = vector(12, 17)
        self.tile_size = vector(32, 32)
        self.tiles = {
            'blank': [0, 8],
            'tree': [0, 9]
            }
        self.tiles = {k: vector(v) for (k, v) in self.tiles.iteritems()}
        self.tile_sheet = pygame.image.load('tiles.png')
        self.player = player

        self.grid = SquareGrid(self.dims)
        self.grid_viewer = SquareGridViewer(self.grid, self.tile_size)
        for row in range(self.dims[0]):
            for col in range(self.dims[1]):
                if random.randint(1, 10) == 1:
                    self.grid.cells[row][col] = self.tiles['tree']
                else:
                    self.grid.cells[row][col] = self.tiles['blank']

    def display(self, dst):
        self.grid_viewer.display(dst)
        
        corner = vector(0, 0)
        for row in range(self.grid.num_rows()):
            for col in range(self.grid.num_cols()):
                tile = self.grid.cells[row][col]
                tile_bounds = (self.tile_size % tile).list()
                tile_bounds += self.tile_size.list()
                pos = corner + 32 * vector(col, row)
                dst.blit(self.tile_sheet, pos.list(), tile_bounds)

        pos = self.player.pos
        self.player.display(dst, self.grid_viewer.get_center(pos))
