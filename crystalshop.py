import pygame
import random

from crystal import *
from crystaldisplay import *
from crystalselector import *
from menu import *
from window import *

class CrystalShop(Window):
    def __init__(self, parent, player):
        Window.__init__(self, parent)
        self.player = player
        self.crystals = [self.make_crystal() for _ in range(30)]
        self.selector = CrystalSelector(self, self.crystals)
        self.crystal_display = CrystalDisplay()

    def make_crystal(self):
        crystal = Crystal()
        if random.randint(1, 3) <= 2:
            elements = ['Neutral', 'Fire', 'Ice', 'Heal', 'Lightning']
            for _ in range(2):
                ele = random.choice(elements)
                mod = random.randint(-5, 3)
                if mod == 0:
                    continue
                crystal.atts[ele] = mod
        crystal.pipes = crystal.random_pipes(1, 1)
        return crystal

    def key_pressed(self, key):
        Window.key_pressed(self, key)

        if key in Menu.select_keys:
            selector = self.selector
            crystal = selector.get_selection()
            if crystal is None:
                return
            selector.remove_selection()
            self.player.crystals.append(crystal)

    def display(self, dst):
        Window.display(self, dst)

        corner = vector(80, 80)
        radius = 20
        self.selector.display(dst, corner, radius)

        crystal = self.selector.get_selection()
        if crystal is not None:
            corner = vector(80, 300)
            self.crystal_display.display(dst, crystal, corner)
