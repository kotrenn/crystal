import pygame
import random

from window import *

class WorldWindow(Window):
    def __init__(self, parent):
        Window.__init__(self, parent)
        self.width = 17
        self.height = 12
        self.tiles = {
            'blank': [0, 8],
            'tree': [0, 9]
            }
        self.tile_sheet = pygame.image.load('tiles.png')

        self.map = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(self.tiles['blank'])
            self.map.append(row)

        for y in range(self.height):
            for x in range(self.width):
                if random.randint(1, 10) == 1:
                    self.map[x][y] = self.tiles['tree']

    def display(self, dst):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.map[x][y]
                tile_bounds = (32 * tile[0], 32 * tile[1], 32, 32)
                offset_x = 20
                offset_y = 20
                dst.blit(self.tile_sheet,
                         (offset_x + x * 32,
                          offset_y + y * 32),
                         tile_bounds)
