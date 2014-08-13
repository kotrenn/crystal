import pygame

from crystal import *
from crystalselector import *
from window import *

class CrystalShop(Window):
    def __init__(self, parent, player):
        Window.__init__(self, parent)
        self.player = player
        self.crystals = [Crystal() for _ in range(5)]
        self.selector = CrystalSelector(self, self.crystals)
        self.crystal_display = CrystalDisplay()

    def key_pressed(self, key):
        Window.key_pressed(self, key)

        if key == pygame.K_x or key == pygame.K_SPACE or key == pygame.K_RETURN:
            selector = self.selector
            crystal = selector.get_selection()
            selector.remove_selection()
            self.player.crystals.append(crystal)

    def display(self, dst):
        Window.display(self, dst)

        corner = vector(80, 80)
        radius = 20
        self.selector.display(dst, corner, radius)

        crystal = self.selector.get_selection()
        corner = vector(80, 300)
        self.crystal_display.display(dst, crystal, corner)
