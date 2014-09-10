from spell import *
from render import *

class SpellSummary(object):
    def __init__(self):
        return

    def display(self, dst, spell, corner):
        if spell is None:
            return

        data = spell.get_atts()
        white = (255, 255, 255)
        draw_string(dst, data, corner, white)
