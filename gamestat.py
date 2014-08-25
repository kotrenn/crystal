class GameStat(object):
    def __init__(self, max_val):
        self.max_val = max_val
        self.val = self.max_val

    def add(self, diff):
        self.val += diff
        self.clamp()

    def sub(self, diff):
        self.val -= diff
        self.clamp()

    def clamp(self):
        if self.val < 0:
            self.val = 0
        elif self.val > self.max_val:
            self.val = self.max_val

    def reset(self):
        self.val = self.max_val

    def __str__(self):
        return '[' + str(self.val) + '/' + str(self.max_val) + ']'
