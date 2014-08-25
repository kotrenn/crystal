from action import *

class AttackAction(Action):
    def __init__(self, actor, target, data):
        Action.__init__(self, actor)
        self.target = target
        self.data = data

    def execute(self):
        if self.data is None:
            return 0
        
        classes = str(type.mro(type(self.target)))
        if ".Monster'" in classes:
            pain = self.data.compute_damage(self.target)
            self.target.take_damage(pain)
        return self.actor
