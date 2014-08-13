import pygame

from vector import *

class CrystalSelector(object):
    def __init__(self, parent, crystals):
        parent.add_key_listener(self)
        self.parent = parent
        self.crystals = crystals
        self.selection = vector(0, 0)
        self.num_cols = 10

    def key_pressed(self, key):
        return

    def key_released(self, key):
        mapping = {
            pygame.K_UP: [0, -1],
            pygame.K_DOWN: [0, 1],
            pygame.K_LEFT: [-1, 0],
            pygame.K_RIGHT: [1, 0]
        }
        if key in mapping and len(self.crystals) > 0:
            vel = vector(mapping[key])
            loc = self.selection + vel
            num_crystals = len(self.crystals)
            num_cols = self.num_cols
            num_rows = num_crystals / num_cols
            loc += vector(num_cols, num_rows + 1)
            loc[0] %= num_cols
            loc[1] %= num_rows + 1
            if loc[0] >= num_crystals % num_cols and \
               loc[1] == num_rows:
                if vel[1] < 0:
                    loc[1] = num_rows - 1
                elif vel[0] != 0:
                    if vel[0] < 0 and self.selection[0] == 0:
                        loc[0] = num_crystals % num_cols - 1
                    else:
                        loc[0] %= num_crystals % num_cols
                else:
                    loc[1] = 0
            self.selection = loc

    def get_offset(self):
        c_row, c_col = self.selection[::-1]
        sel = c_row * self.num_cols + c_col
        return sel

    def add_crystal(self, crystal):
        self.crystals.append(crystal)

    def get_selection(self):
        sel = self.get_offset()
        if sel < 0 or sel >= len(self.crystals):
            return None
        crystal = self.crystals[sel]
        return crystal

    def remove_selection(self):
        sel = self.get_offset()
        if sel < 0 or sel >= len(self.crystals):
            return None
        self.crystals.pop(sel)
        return sel

    def display(self, dst, corner, radius):
        if len(self.crystals) == 0:
            return
        crystal_skip = 3 * radius
        row = col = 0
        num_cols = self.num_cols
        for (i, crystal) in enumerate(self.crystals):
            center = corner + crystal_skip * vector(col, row)
            crystal.display(dst, center, radius)
            col += 1
            if col >= num_cols:
                col = 0
                row += 1
        loc = self.selection
        center = corner + crystal_skip * loc
        skip = crystal_skip * vector(1, 1)
        corner = center - 0.5 * crystal_skip * vector(1, 1)
        dims = corner.list() + skip.list()
        white = (255, 255, 255)
        pygame.draw.rect(dst, white, dims, 1)
