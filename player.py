import pygame

from attackaction import *
from attackdata import *
from color import *
from gamestat import *
from actor import *
from spell import *
from vector import *

class Player(Actor):
    def __init__(self, world):
        Actor.__init__(self, world)
        self.hp = GameStat(20)
        self.mana = [GameStat(10) for _ in range(3)]
        self.crystals = []
        self.spells = []
        for size in [2, 3, 4]:
            self.spells.append(Spell(self, size))
        self.next_action = None

        # create the initial basic melee spell
        basic = self.spells[0]
        color = Color(True, True, True)
        row, col = 1, 1
        crystal = Crystal()
        crystal.color = color
        crystal.pipes = ['In'] * 3 + [None] * 3
        crystal.atts['Cast'] = ['Melee']
        crystal.atts['Neutral'] = 1
        crystal.atts['Mana'] = Color()
        for _ in range(2):
            crystal.rotate(-1)
        basic.grid.cells[row][col] = crystal

    def needs_input(self):
        return self.next_action == None

    def get_action(self):
        action = self.next_action
        self.next_action = None
        return action

    def get_mana(self):
        return Color([x.val for x in self.mana])

    def burn_mana(self, mana_cost):
        for (mana, cost) in zip(self.mana, mana_cost):
            mana.sub(cost)

    def default_attack(self, target):
        data = AttackData()
        data.atts['Neutral'] = 10
        return AttackAction(self, target, data)
