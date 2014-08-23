from playercontroller import *
from window import *
from worldviewer import *

class Explore(Window):
    def __init__(self, parent, world, player):
        Window.__init__(self, parent)
        self.world = world
        self.world_viewer = WorldViewer(world)
        self.player = player
        self.player_controller = PlayerController(self, player, world)
        self.countdown = 0
        self.current_actor = 0

    def advance_actor(self):
        num_actors = len(self.world.actors)
        self.current_actor = (self.current_actor + 1) % num_actors

    def update(self):
        action = None
        while action is None:
            actor = self.world.actors[self.current_actor]
            if actor.energy.gain(actor.get_speed()):
                action = actor.get_action()
            else:
                self.advance_actor()
        action.execute()
        self.advance_actor()
        
    def display(self, dst):
        self.world_viewer.display(dst)

        loc = self.player.loc
        pos = self.world_viewer.grid_viewer.get_center(loc)
        self.player.display(dst, pos)

        for actor in self.world.actors:
            loc = actor.loc
            pos = self.world_viewer.grid_viewer.get_center(loc)
            actor.display(dst, pos)
