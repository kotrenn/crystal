from action import *

class AttackAction(Action):
    def __init__(self, actor, target):
        Action.__init__(self, actor)
        self.target = target

    def execute(self):
        classes = str(type.mro(type(self.target)))
        if ".Monster'" in classes:
            self.target.loc = self.target.world.random_open()
        return self.actor
