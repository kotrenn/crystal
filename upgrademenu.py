from crystaldisplay import *
from crystalselector import *
from menu import *

class UpgradeMenu(Menu):
    def __init__(self, parent, player):
        options = ['Manipulate', 'Red', 'Green', 'Blue', 'Back']
        Menu.__init__(self, parent, options)
        self.player = player
        self.buffer = []
        self.buffer_selector = CrystalSelector(self, self.buffer)
        self.player_selector = CrystalSelector(self, self.player.crystals)
        self.cur_selector = self.player_selector
        self.other_selector = self.buffer_selector
        self.cur_selector.selecting = False
        self.other_selector.selecting = False
        self.buffer_selector.num_cols = 5
        self.player_selector.num_cols = 5
        self.crystal_display = CrystalDisplay()
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
            selector.crystals.append(crystal)
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

        mapping = {
            'Red': 0,
            'Green': 1,
            'Blue': 2
        }
        if not msg in mapping:
            return
        index = mapping[msg]
        color = Color(0, 0, 0)
        color[index] = 1
        mana = self.player.mana[index]
        match = filter(lambda x: color <= x.color, self.buffer)
        count = len(match)
        print 'Adding ' + str(count) + ' mana to ' + msg
        mana.max_val += count
        mana.add(count)
        for crystal in match:
            self.buffer.remove(crystal)
        
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
            self.crystal_display.display(dst, crystal, corner)
