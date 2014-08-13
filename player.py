class Player(object):
    def __init__(self):
        self.hp_max = 5
        self.hp = self.hp_max
        self.mana = [10, 10, 10]
        self.pos = [0, 0]
        self.crystals = []
