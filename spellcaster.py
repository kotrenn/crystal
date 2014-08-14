class SpellCaster(object):
    def __init__(self, world, player, spell):
        self.world = world
        self.player = player
        self.spell = spell

    def csat(self):
        mana = self.spell.get_mana_cost()
        if not self.player.has_mana(mana):
            return
        self.player.remove_mana(mana)
