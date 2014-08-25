from action import *
from projectile import *

class CastSpellAction(Action):
    def __init__(self, actor, spell, dir):
        Action.__init__(self, actor)
        self.spell = spell
        self.dir = dir

    def execute(self):
        world = self.actor.world
        loc = self.actor.loc
        vel = world.grid.dir_vel(self.dir)
        projectile = Projectile(world, loc + vel, self.dir)
        projectile.set_world(world)
