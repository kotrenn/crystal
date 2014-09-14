class Action(object):
    def __init__(self, actor):
        self.actor = actor
        self.level = actor.level

    def execute(self):
        return None
