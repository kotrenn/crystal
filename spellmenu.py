from menu import *
from spelleditor import *

class SpellMenu(Menu):
    def __init__(self, parent, player):
        spells = player.spells
        options = []
        for (i, spell) in enumerate(spells):
            opt = 'Spell ' + str(i + 1) + ' (' + str(spell.size) + ')'
            options.append(opt)
        options += ['Back']
        Menu.__init__(self, parent, options)
        self.player = player

    def select(self, msg):
        if msg == 'Back':
            self.exit()
        else:
            sel = self.selection
            spell = self.player.spells[sel]
            editor = SpellEditor(self, spell)
            self.child = editor
