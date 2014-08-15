from settings import *
from spell import *
from vector import *

class Player(object):
    def __init__(self):
        self.hp_max = 5
        self.hp = self.hp_max
        self.mana = [10, 10, 10]
        self.loc = vector([0, 0])
        self.crystals = []
        self.spells = []
        for size in [2, 3, 4]:
            self.spells.append(Spell(self, size))

    def display(self, dst, center):
        settings = Settings()
        font = settings.font
        color = (255, 255, 255)
        text = font.render('@', True, color)
        loc = center - 0.5 * vector(text.get_size())
        dst.blit(text, loc.list())
