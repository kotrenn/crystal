from action import *

class TalkAction(Action):
    def __init__(self, actor, target):
        Action.__init__(self, actor)
        self.target = target

    def execute(self):
        self.target.talk_to(self.actor)
