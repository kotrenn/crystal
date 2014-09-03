from actor import *
from gamestat import *
from squaregrid import *
from walkaction import *

class NPC(Actor):
    def __init__(self, world):
        Actor.__init__(self, world)
        self.speed = Energy.NORMAL_SPEED
        self.hp = GameStat(1)
        self.loc = self.world.random_empty()

    def get_color(self):
        return (0, 255, 255)

    def get_action(self):
        return WalkAction(self, DIR_NONE)

    def talk_to(self, source):
        print 'You talked to the NPC!'
        return
