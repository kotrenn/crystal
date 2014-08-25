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
        start = loc + vel
        if world.is_blocked(start):
            return
        data = self.spell.get_attack()
        mana = data.atts['Mana']
        if not mana <= self.actor.get_mana():
            return
        if 'Cast' not in data.atts:
            return
        instant = False
        if 'Melee' in data.atts['Cast']:
            instant = True
        self.actor.burn_mana(mana)
        projectile = Projectile(world, start, self.dir, data, instant)
