from action import *

class AttackAction(Action):
    def __init__(self, actor, target, data):
        Action.__init__(self, actor)
        self.target = target
        self.data = data

    def execute(self):
        if self.data is None:
            return 0

        if self.target.has_class('Monster'):
            pain = self.data.compute_damage(self.target)
            self.target.take_damage(pain)
        return self.actor
