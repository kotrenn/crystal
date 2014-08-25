class Action(object):
    def __init__(self, actor):
        self.actor = actor
        self.world = actor.world

    def execute(self):
        return None
