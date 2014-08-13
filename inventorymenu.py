from menu import *

class InventoryMenu(Menu):
    def __init__(self, parent, player):
        crystals = {}
        for crystal in player.crystals:
            color = crystal.color
            if color in crystals:
                crystals[color] += 1
            else:
                crystals[color] = 1
        title = {
            (255, 0, 0): 'Red',
            (0, 255, 0): 'Green',
            (0, 0, 255): 'Blue'
            }
        options = [str(title[k]) + ' x' + str(v) for (k, v) in crystals.iteritems()]
        options += ['Back']
        Menu.__init__(self, parent, options)
        self.player = player

    def select(self, msg):
        if msg == 'Back':
            self.exit()
