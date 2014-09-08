from crystalsummary import *
from itemselector import *
from menu import *

class UpgradeMenu(Menu):
    def __init__(self, parent, player):
        options = ['Manipulate', 'Health', 'Mana', 'Mana Regen', 'Back']
        Menu.__init__(self, parent, options)
        self.player = player
        self.buffer = []
        self.buffer_selector = ItemSelector(self, self.buffer)
        self.player_selector = ItemSelector(self, self.player.crystals)
        self.cur_selector = self.player_selector
        self.other_selector = self.buffer_selector
        self.cur_selector.selecting = False
        self.other_selector.selecting = False
        self.buffer_selector.num_cols = 5
        self.player_selector.num_cols = 5
        self.crystal_summary = CrystalSummary()
        self.selecting = False

    def key_released(self, key):
        if not self.selecting:
            Menu.key_released(self, key)
            return

        if self.selecting:
            if key == pygame.K_ESCAPE:
                self.selecting = False
                self.cur_selector.selecting = False
                return

        self.cur_selector.key_released(key)

        if key in Menu.select_keys:
            selector = self.cur_selector
            crystal = selector.get_selection()
            if crystal is None:
                return
            selector.remove_selection()
            selector = self.other_selector
            selector.add_item(crystal)
            return

        if key == pygame.K_s:
            self.cur_selector.selecting = False
            self.other_selector.selecting = True
            self.cur_selector, self.other_selector \
                = self.other_selector, self.cur_selector

    def exit(self):
        for crystal in self.buffer:
            self.player.crystals.append(crystal)
        Menu.exit(self)

    def select(self, msg):
        if msg == 'Back':
            self.exit()

        if msg == 'Manipulate':
            self.selecting = True
            self.cur_selector.selecting = True
            return

        

        if msg == 'Health':
            delta = Color(0, 0, 0)
            for crystal in self.buffer:
                delta += crystal.color
            hp_gain = min(delta.tuple(1))
            hp = self.player.hp
            hp.max_val += hp_gain
            hp.add(hp_gain)
            #delta -= Color([hp_gain] * 3)
            while len(self.buffer) > 0 and delta > Color():
                crystal = self.buffer.pop()
                delta -= crystal.color
                
        if msg == 'Mana':
            delta = Color(0, 0, 0)
            for crystal in self.buffer:
                delta += crystal.color
            for i in range(3):
                mana = self.player.mana[i]
                mana.max_val += delta[i]
                mana.add(delta[i])
            while len(self.buffer) > 0:
                self.buffer.pop()

        if msg == 'Mana Regen':
            delta = Color(0, 0, 0)
            for crystal in self.buffer:
                delta += crystal.color
            self.player.mana_gen += delta
            while len(self.buffer) > 0:
                self.buffer.pop()
        
    def display(self, dst):
        Menu.display(self, dst)

        corner = vector(160, 40)
        radius = 20
        self.buffer_selector.display(dst, corner, radius)
        offset_x = 3 * radius * self.buffer_selector.num_cols
        offset_x += 20
        corner += vector(offset_x, 0)
        self.player_selector.display(dst, corner, radius)

        crystal = self.cur_selector.get_selection()
        if crystal is not None:
            corner = vector(20, 300)
            self.crystal_summary.display(dst, crystal, corner)
