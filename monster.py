import random

from action import *
from actor import *
from squaregrid import *

class Monster(Actor):
    def __init__(self, world):
        Actor.__init__(self, world)

    def get_action(self):
        dir = random.choice([DIR_NW, DIR_N,
                             DIR_NE, DIR_E,
                             DIR_SE, DIR_S,
                             DIR_SW, DIR_W])
        vel = self.world.grid.dir_vel(dir)
        return WalkAction(self, vel)
        
    def get_color(self):
        return (255, 0, 0)
