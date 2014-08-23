import pygame

from playercontroller import *
from squaregridviewer import *
from vector import *
from window import *
from world import *

class WorldViewer(Window):
    def __init__(self, parent, world, player):
        Window.__init__(self, parent)
        self.world = world
        self.tile_size = vector(32, 32)
        self.tile_sheet = pygame.image.load('tiles.png')
        self.player = player
        self.player_controller = PlayerController(self, player, world)

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
                pos = corner + 32 * vector(col, row)
                dst.blit(self.tile_sheet, pos.list(), tile_bounds)

        loc = self.player.loc
        self.player.display(dst, self.grid_viewer.get_center(loc))
