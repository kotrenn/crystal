from actor import *
from attackaction import *
from energy import *
from walkaction import *

class Projectile(Actor):
    def __init__(self, world, loc, dir, data):
        Actor.__init__(self, world)
        self.loc = loc
        self.dir = dir
        self.speed = Energy.MAX_SPEED
        self.data = data
        self.die_at_wall = True

        target = self.world.actor_at(self.loc)
        if target is not None:
            if target.has_class('Monster'):
                action = self.default_attack(target)
                action.execute()

    def get_action(self):
        return WalkAction(self, self.dir)

    def get_symbol(self):
        return '*'

    def get_color(self):
        return (0, 0, 255)

    def default_attack(self, target):
        self.world.remove_actor(self)
        return AttackAction(self, target, self.data)
    
