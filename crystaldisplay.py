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
            val_str = str(v)
            if isinstance(v, (int, long)):
                val_str = '{:+d}'.format(v)
            data += str(k) + ': ' + val_str + '\n'
        color = crystal.color.tuple(255)
        draw_string(dst, data, corner, color)
