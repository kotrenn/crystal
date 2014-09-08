from itemselector import *
from recipeparser import *
from render import *
from settings import *
from window import *

class RecipeViewer(Window):
    def __init__(self, parent, recipe, player):
        Window.__init__(self, parent)
        self.recipe = recipe
        self.player = player
        self.cost_selectors = []
        self.input_selectors = []
        self.crystal_selector = ItemSelector(self, self.player.crystals)
        self.spell_selector = ItemSelector(self, self.player.spells)

        self.build_selectors(self.cost_selectors,
                             self.recipe.cost)
        self.build_selectors(self.input_selectors,
                             self.recipe.input)

    def build_selectors(self, selector_list, vars):
        for var in vars:
            items = []
            selector = ItemSelector(self, items)
            if var.count.isdigit():
                count = int(var.count)
                selector.max_size = count
                selector.num_cols = min(10, count)
            selector_list.append(selector)

    def display(self, dst):
        # draw the title
        label = self.recipe.label
        white = (255, 255, 255)
        pos = (20, 20)
        draw_string(dst, label, pos, white)

        # draw selectors
        settings = Settings()
        font = settings.font
        corner = vector(80, 80)
        radius = 20
        selector_skip = vector(0, 3 * radius)
        selectors = []
        selectors += zip(self.input_selectors, self.recipe.input)
        selectors += zip(self.cost_selectors, self.recipe.cost)
        selectors += [(self.crystal_selector, 'crystals')]
        selectors += [(self.spell_selector, 'spells')]
        for (selector, var) in selectors:
            cur_radius = radius
            selector.display(dst, corner, radius)
            if var is not None:
                text = font.render(str(var), True, white)
                #text_pos = corner - vector(text.get_size()) - vector(20, 0)
                text_pos = corner
                dst.blit(text, text_pos.list())
            corner += selector_skip * selector.num_rows()
