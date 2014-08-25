from crystal import *
from render import *

class CrystalDisplay(object):
    def __init__(self):
        return

    def display(self, dst, crystal, corner):
        if crystal is None:
            return
            
        data = ''
        for (k, v) in crystal.atts.iteritems():
            data += str(k) + ': ' + str(v) + '\n'
        color = crystal.color.tuple()
        draw_string(dst, data, corner, color)
