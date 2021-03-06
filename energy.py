class Energy(object):
    MIN_SPEED = 0
    NORMAL_SPEED = 3
    MAX_SPEED = 5
    
    ACTION_COST = 12

    GAINS = [
        2,  # 1/3 normal speed
        3,  # 2/3 normal speed
        4,
        6,  # normal speed
        9,
        12  # 2x speed
    ]
    
    def __init__(self):
        self.energy = 0

    def can_take_turn(self):
        return self.energy >= Energy.ACTION_COST

    def gain(self, speed):
        self.energy += Energy.GAINS[speed]
        return self.can_take_turn()

    def spend(self):
        self.energy %= Energy.ACTION_COST
