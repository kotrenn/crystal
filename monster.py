import random

from action import *
from actor import *
from squaregrid import *

class Monster(Actor):
    def __init__(self, world):
        Actor.__init__(self, world)
        if random.randint(1, 3) == 1:
            self.speed = Energy.MIN_SPEED
        else:
            self.speed = Energy.MAX_SPEED
        self.dst = vector(0, 0)
        self.random_dst()

    def random_dst(self):
        dst = [random.randint(0, self.world.dims[0] - 1),
               random.randint(0, self.world.dims[1] - 1)]
        self.dst = vector(dst)

    def get_action(self):
        dir = random.choice([DIR_NW, DIR_N,
                             DIR_NE, DIR_E,
                             DIR_SE, DIR_S,
                             DIR_SW, DIR_W])
        vel = self.world.grid.dir_vel(dir)

        if self.loc == self.dst:
            self.random_dst()
        
        dir = self.world.a_star(self.loc, self.dst)
        vel = self.world.grid.dir_vel(dir)
        
        return WalkAction(self, vel)
        
    def get_color(self):
        return (255, 0, 0)
