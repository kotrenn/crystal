from craftmenu import *
from crystalshop import *
from explore import *
from inventorymenu import *
from menu import *
from spell import *
from spellmenu import *
from world import *
from worldviewer import *

class MainMenu(Menu):
    def __init__(self, player):
        Menu.__init__(self, None,
                      ['Buy Crystals', 'Inventory', 'Explore', 'Crafting', 'Spells', 'World', 'Quit'])
        self.image = pygame.image.load('splash.png')
        self.player = player
        self.level = Level()
        self.world = World(800, 600, 100)

    def select(self, msg):
        if msg == 'Quit':
            self.exit()
        elif msg == 'Buy Crystals':
            self.child = CrystalShop(self, self.player)
        elif msg == 'Inventory':
            self.child = InventoryMenu(self, self.player)
        elif msg == 'Explore':
            self.child = Explore(self, self.level, self.player)
        elif msg == 'Crafting':
            self.child = CraftMenu(self, self.player)
        elif msg == 'Spells':
            self.child = SpellMenu(self, self.player)
        elif msg == 'World':
            self.child = WorldViewer(self, self.world)

    def render_image(self):
        return self.image
