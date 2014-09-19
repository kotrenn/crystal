import pygame

from vector import *

class ItemSelector(object):
    def __init__(self, parent, items):
        parent.add_key_listener(self)
        self.parent = parent
        self.items = items
        self.selecting = True
        self.selection = vector(0, 0)
        self.num_cols = 10
        self.max_size = None
        self.max_rows = None
        self.allowed_types = []

    def add_type(self, typename):
        self.allowed_types.append(typename)

    def is_allowed(self, item):
        return item.type in self.allowed_types

    def has_space(self):
        if self.max_size is None:
            return True
        return self.num_items() < self.max_size

    def key_pressed(self, key):
        return

    def num_rows(self):
        return 1 + self.num_items() / self.num_cols

    def num_items(self):
        return len(self.items)

    def visible_rows(self):
        ret = self.num_rows()
        if self.num_items() % self.num_cols == 0:
            ret -= 1
        return max(1, ret)

    def key_released(self, key):
        if not self.selecting:
            return
        
        mapping = {
            pygame.K_UP: [0, -1],
            pygame.K_DOWN: [0, 1],
            pygame.K_LEFT: [-1, 0],
            pygame.K_RIGHT: [1, 0]
        }
        if key in mapping and self.num_items() > 0:
            vel = vector(mapping[key])
            loc = self.selection + vel
            num_items = self.num_items()
            num_cols = self.num_cols
            num_rows = self.num_rows()
            loc += vector(num_cols, num_rows)
            loc[0] %= num_cols
            loc[1] %= num_rows
            if loc[0] >= num_items % num_cols and \
               loc[1] == num_rows - 1:
                if vel[1] < 0:
                    loc[1] = num_rows - 2
                elif vel[0] != 0:
                    if vel[0] < 0 and self.selection[0] == 0:
                        loc[0] = num_items % num_cols - 1
                    else:
                        loc[0] %= num_items % num_cols
                else:
                    loc[1] = 0
            self.selection = loc

    def get_offset(self):
        c_row, c_col = self.selection.transpose().tuple()
        sel = c_row * self.num_cols + c_col
        return sel

    def add_item(self, item, check_limit=False):
        if check_limit:
            if not self.has_space():
                return False
        self.items.append(item)
        return True

    def get_selection(self):
        sel = self.get_offset()
        if sel < 0 or sel >= self.num_items():
            return None
        item = self.items[sel]
        return item

    def remove_selection(self):
        sel = self.get_offset()
        if sel < 0 or sel >= self.num_items():
            return None
        self.items.pop(sel)
        return sel

    def remove_item(self, item):
        self.items.remove(item)

    def clear(self):
        while self.num_items() > 0:
            self.remove_item(self.items[-1])

    def display(self, dst, corner, radius):
        white = (255, 255, 255)
        self.draw_bounds(dst, white, corner, radius)
        
        if self.num_items() == 0:
            return

        # draw the items
        item_skip = 3 * radius
        row = col = 0
        num_cols = self.num_cols
        for (i, item) in enumerate(self.items):
            center = corner + item_skip * vector(col, row)
            item.display(dst, center, radius)
            col += 1
            if col >= num_cols:
                col = 0
                row += 1

        # draw a box around the currently selected item
        if not self.selecting:
            return
        loc = self.selection
        center = corner + item_skip * loc
        skip = item_skip * vector(1, 1)
        corner = center - 0.5 * item_skip * vector(1, 1)
        dims = corner.list() + skip.list()
        pygame.draw.rect(dst, white, dims, 1)

    def draw_bounds(self, dst, color, corner, radius, shrink=0):
        item_skip = 3 * radius
        corner = corner - 0.5 * item_skip * vector(1, 1)
        corner += shrink * vector(1, 1)
        dims = item_skip * vector(self.num_cols, self.visible_rows())
        dims -= 2 * shrink * vector(1, 1)
        rect = corner.list() + dims.list()
        pygame.draw.rect(dst, color, rect, 1)
