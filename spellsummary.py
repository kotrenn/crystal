# Simple interface for collecting and displaying information about a
# spell based on the current setup within the spell.

from spell import *
from render import *

class SpellSummary(object):
    def __init__(self):
        return

    # Render to the screen
    def display(self, dst, spell, corner):
        # Sanity check
        if spell is None:
            return

        # Simple version:  collect list of attributes and display as a string
        data = spell.get_atts()
        white = (255, 255, 255)
        draw_string(dst, data, corner, white)
