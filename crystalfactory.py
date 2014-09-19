import random

from crystal import *

class CrystalFactory(object):
    def __init__(self):
        return

    def make_crystal(self):
        return

    def random_pipes(self, num_in, num_out):
        # variance on num_in and num_out
        while random.randint(1, 5) == 1:
            num_in += random.choice([1] * 3 + [-1])
        while random.randint(1, 5) == 1:
            num_out += random.choice([1] * 3 + [-1])

        # scale to total of 6 and ensure at least one input
        if num_in < 1: num_in = 1
        if num_out < 0: num_out = 0
        total = num_in + num_out
        if total > 6:
            num_in = 6 * num_in / total
            if num_in < 1: num_in = 1
            num_out = 6 - num_in
            total = num_in + num_out

        # build the actual list
        ret = ['In'] * num_in
        ret += ['Out'] * num_out
        ret += [None] * (6 - total)
        random.shuffle(ret)
        if len(ret) != 6:
            print 'ERROR: ' + str(ret) + ' ' + str(old)
        return ret

class BasicCrystalFactory(CrystalFactory):
    def __init__(self):
        CrystalFactory.__init__(self)

    def make_crystal(self):
        crystal = Crystal()

        # add damage modifiers
        if random.randint(1, 3) <= 2:
            elements = ['Neutral', 'Fire', 'Ice', 'Heal', 'Lightning']
            for _ in range(2):
                ele = random.choice(elements)
                mod = random.randint(-2, 4)
                if mod == 0:
                    continue
                crystal.atts[ele] = mod

        # set pipes
        crystal.pipes = self.random_pipes(1, 1)

        # done
        return crystal
