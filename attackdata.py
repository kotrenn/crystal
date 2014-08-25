class AttackData(object):
    def __init__(self):
        self.atts = {}

    def compute_damage(self, target):
        ret = 0
        modifiers = ['Fire', 'Ice', 'Lightning']
        for mod in modifiers:
            if not mod in self.atts:
                continue
            ret += self.atts[mod]
        if ret < 0:
            ret = 0
        return ret
