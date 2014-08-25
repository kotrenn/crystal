from playercontroller import *
from window import *
from worldviewer import *
from world import *

class Explore(Window):
    def __init__(self, parent, world, player):
        Window.__init__(self, parent)
        self.world = world
        self.world_viewer = WorldViewer(world)
        self.player = player
        self.player.set_world(world)
        self.player_controller = PlayerController(self, player, world)
        self.current_actor = 0

    def advance_actor(self):
        num_actors = len(self.world.actors)
        self.current_actor = (self.current_actor + 1) % num_actors

    def update(self):
        action = None
        while action is None:
            actor = self.world.actors[self.current_actor]
            if actor.energy.can_take_turn() and actor.needs_input():
                return
            if actor.energy.can_take_turn() or \
               actor.energy.gain(actor.get_speed()):
                if actor.needs_input():
                    return
                action = actor.get_action()
            else:
                self.advance_actor()
        action.execute()
        self.advance_actor()
        
    def display(self, dst):
        self.world_viewer.display(dst)

        for actor in self.world.actors:
            loc = actor.loc
            pos = self.world_viewer.grid_viewer.get_center(loc)
            actor.display(dst, pos)
