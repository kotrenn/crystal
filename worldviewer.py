import pygame

from squaregridviewer import *
from vector import *
from world import *

class WorldViewer(object):
    def __init__(self, world):
        self.world = world
        self.tile_size = vector(32, 32)
        self.tile_sheet = pygame.image.load('tiles.png')
        self.grid_viewer = SquareGridViewer(self.world.grid,
                                            self.tile_size)

    def display(self, dst):
        self.grid_viewer.display(dst)
        
        corner = vector(0, 0)
        grid = self.world.grid
        for row in range(grid.num_rows()):
            for col in range(grid.num_cols()):
                tile = grid.cells[row][col]
                tile_bounds = (self.tile_size % tile).list()
                tile_bounds += self.tile_size.list()
                pos = corner + self.tile_size % vector(col, row)
                dst.blit(self.tile_sheet, pos.list(), tile_bounds)
