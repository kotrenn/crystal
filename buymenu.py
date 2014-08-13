from crystalmenu import *
from menu import *

class BuyMenu(Menu):
    def __init__(self, parent, player):
        Menu.__init__(self, parent, ['Crystals', 'Weapons', 'Back'])
        self.player = player

    def select(self, msg):
        if msg == 'Back':
            self.exit()
        elif msg == 'Crystals':
            self.child = CrystalMenu(self, self.player)
