class Action(object):
    def __init__(self, actor):
        self.actor = actor
        self.world = actor.world

    def execute(self):
        return None

class WalkAction(Action):
    def __init__(self, actor, vel):
        Action.__init__(self, actor)
        self.vel = vel

    def execute(self):
        loc = self.actor.loc + self.vel
        if self.world.is_blocked(loc):
            return None
        self.actor.loc = loc
        return self.actor
