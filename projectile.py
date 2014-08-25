from actor import *
from attackaction import *
from energy import *
from walkaction import *

class Projectile(Actor):
    def __init__(self, world, loc, dir):
        Actor.__init__(self, world)
        self.loc = loc
        self.dir = dir
        self.speed = Energy.MAX_SPEED

    def get_action(self):
        return WalkAction(self, self.dir)

    def get_symbol(self):
        return '*'

    def get_color(self):
        return (0, 0, 255)

    def default_attack(self, target):
        return AttackAction(self, target)
    
