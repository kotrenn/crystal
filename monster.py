import random

from actor import *
from attackaction import *
from squaregrid import *
from walkaction import *

class Monster(Actor):
    def __init__(self, world):
        Actor.__init__(self, world)
        if random.randint(1, 3) == 1:
            self.speed = Energy.MIN_SPEED
        else:
            self.speed = Energy.MAX_SPEED

    def get_action(self):
        dir = self.world.a_star(self.loc, self.world.player.loc)
        if dir == DIR_NONE:
            return WalkAction(self, dir)

        vel = self.world.grid.dir_vel(dir)
        new_loc = self.loc + vel
        if self.world.actor_at(new_loc):
            return WalkAction(self, DIR_NONE)
        
        return WalkAction(self, dir)

    def default_attack(self, target):
        return AttackAction(self, target)
        
    def get_color(self):
        return (255, 0, 0)
