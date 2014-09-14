import random

from actor import *
from attackaction import *
from crystal import *
from crystalfactory import *
from gamestat import *
from squaregrid import *
from walkaction import *

class Monster(Actor):
    def __init__(self, level):
        Actor.__init__(self, level)
        self.speed = Energy.NORMAL_SPEED
        self.hp = GameStat(1)
        self.loc = self.level.random_empty()
        self.crystal_factory = BasicCrystalFactory()

    def get_action(self):
        dir = self.level.a_star(self.loc, self.level.player.loc)
        if dir == DIR_NONE:
            return WalkAction(self, dir)

        vel = self.level.grid.dir_vel(dir)
        new_loc = self.loc + vel
        if self.level.actor_at(new_loc):
            return WalkAction(self, DIR_NONE)
        
        return WalkAction(self, dir)

    def default_attack(self, target, dir):
        return AttackAction(self, target, None)
        
    def get_color(self):
        return (255, 0, 0)
        
    def take_damage(self, damage):
        self.hp.sub(damage)
        if self.hp.val <= 0:
            self.die()

    def die(self):
        self.hp.max_val += 1
        self.hp.reset()
        if random.randint(1, 3) == 1:
            crystal = self.crystal_factory.make_crystal()
            row, col = self.loc.tuple()
            self.level.items.cells[row][col].append(crystal)
        self.loc = self.level.random_empty()
