import pygame

from action import *
from actor import *
from spell import *
from vector import *

class Player(Actor):
    def __init__(self, world):
        Actor.__init__(self, world)
        self.hp_max = 5
        self.hp = self.hp_max
        self.mana = [10, 10, 10]
        self.crystals = []
        self.spells = []
        for size in [2, 3, 4]:
            self.spells.append(Spell(self, size))
        self.next_action = None

    def needs_input(self):
        return self.next_action == None

    def get_action(self):
        action = self.next_action
        self.next_action = None
        return action

    def default_attack(self, target):
        return AttackAction(self, target)
