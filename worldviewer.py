import pygame

from window import *
from world import *

class WorldViewer(Window):
    def __init__(self, parent, world):
        Window.__init__(self, parent)
        self.world = world
        
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
