from actor import *
from attackaction import *
from energy import *
from walkaction import *

class Projectile(Actor):
    def __init__(self, level, loc, dir, data, instant = False):
        Actor.__init__(self, level)
        self.loc = loc
        self.dir = dir
        self.speed = Energy.MAX_SPEED
        self.data = data
        self.die_at_wall = True
        self.instant = instant

        target = self.level.actor_at(self.loc)
        if target is not None:
            if not target.has_class('Monster'):
                return
            action = self.default_attack(target, self.dir)
            action.execute()
            if self.instant:
                self.level.remove_actor(self)

    def get_action(self):
        ret = WalkAction(self, self.dir)
        if self.instant:
            self.level.remove_actor(self)
        return ret

    def get_symbol(self):
        return '*'

    def get_color(self):
        return (0, 0, 255)

    def default_attack(self, target, dir):
        self.level.remove_actor(self)
        return AttackAction(self, target, self.data)
    
