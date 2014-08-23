from crystalshop import *
from inventorymenu import *
from menu import *
from spell import *
from spellmenu import *
from worldviewer import *

class MainMenu(Menu):
    def __init__(self, player):
        Menu.__init__(self, None,
                      ['Buy Crystals', 'Inventory', 'Explore', 'Upgrade', 'Spells', 'Quit'])
        self.image = pygame.image.load('splash.png')
        self.player = player
        self.world = World()

    def select(self, msg):
        if msg == 'Quit':
            self.exit()
        elif msg == 'Buy Crystals':
            self.child = CrystalShop(self, self.player)
        elif msg == 'Inventory':
            self.child = InventoryMenu(self, self.player)
        elif msg == 'Explore':
            self.child = WorldViewer(self, self.world, self.player)
        elif msg == 'Spells':
            self.child = SpellMenu(self, self.player)

    def render_image(self):
        return self.image
