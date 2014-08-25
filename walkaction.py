from action import *

class WalkAction(Action):
    def __init__(self, actor, dir):
        Action.__init__(self, actor)
        self.dir = dir

    def execute(self):
        vel = self.world.grid.dir_vel(self.dir)
        loc = self.actor.loc + vel
        if self.world.is_blocked(loc):
            return None
        target = self.world.actor_at(loc)
        if target is not None and target is not self.actor:
            action = self.actor.default_attack(target)
            ret = None
            if action is not None:
                ret = action.execute()
            return ret
        self.actor.loc = loc
        return self.actor
