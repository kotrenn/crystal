from action import *
from actor import *
from energy import *
import action

class Projectile(Actor):
    def __init__(self, world, loc, dir):
        Actor.__init__(self, world)
        self.loc = loc
        self.dir = dir
        self.speed = Energy.MAX_SPEED

    def get_action(self):
        return action.WalkAction(self, self.dir)

    def get_symbol(self):
        return '*'

    def get_color(self):
        return (0, 0, 255)

    def default_attack(self, target):
        return action.AttackAction(self, target)
    
