class Action(object):
    def __init__(self, actor):
        self.actor = actor
        self.world = actor.world

    def execute(self):
        return None

class WalkAction(Action):
    def __init__(self, actor, dir):
        Action.__init__(self, actor)
        self.dir = dir

    def execute(self):
        vel = self.world.grid.dir_vel(self.dir)
        loc = self.actor.loc + vel
        if self.world.is_blocked(loc):
            return None
        self.actor.loc = loc
        return self.actor
