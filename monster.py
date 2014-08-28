import random

from actor import *
from attackaction import *
from crystal import *
from gamestat import *
from squaregrid import *
from walkaction import *

class Monster(Actor):
    def __init__(self, world):
        Actor.__init__(self, world)
        self.speed = Energy.NORMAL_SPEED
        self.hp = GameStat(1)
        self.loc = self.world.random_empty()

    def get_action(self):
        dir = self.world.a_star(self.loc, self.world.player.loc)
        if dir == DIR_NONE:
            return WalkAction(self, dir)

        vel = self.world.grid.dir_vel(dir)
        new_loc = self.loc + vel
        if self.world.actor_at(new_loc):
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
            crystal = Crystal()
            if random.randint(1, 3) <= 2:
                elements = ['Neutral', 'Fire', 'Ice', 'Heal', 'Lightning']
                for _ in range(2):
                    ele = random.choice(elements)
                    mod = random.randint(-2, 4)
                    if mod == 0:
                        continue
                    crystal.atts[ele] = mod
            crystal.pipes = crystal.random_pipes(1, 1)
            row, col = self.loc.tuple()
            self.world.items.cells[row][col].append(crystal)
        self.loc = self.world.random_empty()
