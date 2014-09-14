from action import *

class GetAction(Action):
    def __init__(self, actor, loc):
        Action.__init__(self, actor)
        self.loc = loc
        
    def execute(self):
        row, col = self.loc.tuple()
        items = self.actor.level.items.cells[row][col]
        if len(items) == 0:
            return None
        for item in items:
            self.actor.crystals.append(item)
        del items[:]
