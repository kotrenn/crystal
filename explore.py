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

    def display(self, dst):
        self.world_viewer.display(dst)

        loc = self.player.loc
        pos = self.world_viewer.grid_viewer.get_center(loc)
        self.player.display(dst, pos)
