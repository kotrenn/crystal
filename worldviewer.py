import pygame

from explore import *
from menu import *
from window import *
from world import *

class WorldViewer(Window):
    def __init__(self, parent, world, player):
        Window.__init__(self, parent)
        self.world = world
        self.player = player

        self.selection = 0

    def key_released(self, key):
        Window.key_released(self, key)

        if key in Menu.select_keys:
            level = self.world.levels[self.selection]
            self.child = Explore(self, level, self.player)
            return
        
        mapping = {
            pygame.K_UP:    [0, -1],
            pygame.K_DOWN:  [0, 1],
            pygame.K_LEFT:  [-1, 0],
            pygame.K_RIGHT: [1, 0]
            }

        if key in mapping:
            vel = vector(mapping[key])
            neighbors = self.world.neighbors(self.selection)
            p0 = self.world.points[self.selection]
            cur_best = None
            max_proj = None
            for v in neighbors:
                p1 = self.world.points[v]
                delta = (p1 - p0).norm()
                proj = delta ** vel
                if proj < 0:
                    continue
                if cur_best is None or proj > max_proj:
                    cur_best = v
                    max_proj = proj
            if cur_best is not None:
                self.selection = cur_best
        
    def display(self, dst):
        world = self.world
        color = (255, 255, 255)
        radius = 5
        for p in world.points:
            pygame.draw.circle(dst, color, p.list(), radius, 1)
        for (u, v) in world.edges:
            p_u = world.points[u].list()
            p_v = world.points[v].list()
            pygame.draw.line(dst, color, p_u, p_v)

        color = (255, 0, 0)
        p = world.points[self.selection]
        dims = 4 * radius * vector(1, 1)
        bounds = p - dims / 2
        bounds = bounds.list() + dims.list()
        pygame.draw.rect(dst, color, bounds, 1)
