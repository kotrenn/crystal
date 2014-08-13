from buymenu import *
from inventorymenu import *
from menu import *
from spell import *
from worldwindow import *
from crystalshop import *

class MainMenu(Menu):
    def __init__(self, player):
        Menu.__init__(self, None,
                      ['Buy Stuff', 'Inventory', 'Explore', 'Upgrade', 'Spell Grid', 'Quit'])
        self.image = pygame.image.load('splash.png')
        self.player = player

    def select(self, msg):
        if msg == 'Quit':
            self.exit()
        elif msg == 'Buy Stuff':
            #self.child = BuyMenu(self, self.player)
            self.child = CrystalShop(self, self.player)
        elif msg == 'Inventory':
            self.child = InventoryMenu(self, self.player)
        elif msg == 'Explore':
            self.child = WorldWindow(self)
        elif msg == 'Spell Grid':
            spell = Spell(self.player)
            editor = SpellEditor(self, spell)
            self.child = editor

    def render_image(self):
        return self.image
