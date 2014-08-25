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
        target = self.world.actor_at(loc)
        if target is not None and target is not self.actor:
            action = self.actor.default_attack(target)
            ret = None
            if action is not None:
                ret = action.execute()
            return ret
        self.actor.loc = loc
        return self.actor

class AttackAction(Action):
    def __init__(self, actor, target):
        Action.__init__(self, actor)
        self.target = target

    def execute(self):
        name = self.target.__class__.__name__
        if name == 'Monster':
            self.target.loc = self.target.world.random_open()
        return self.actor
