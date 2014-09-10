from itemselector import *
from menu import *
from recipeparser import *
from recipewalker import *
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
        self.crystal_selector.selecting = False
        self.spell_selector = ItemSelector(self, self.player.spells)
        self.spell_selector.selecting = False

        self.build_selectors(self.cost_selectors,
                             self.recipe.cost)
        self.build_selectors(self.input_selectors,
                             self.recipe.input)

        self.cur_selector = None
        self.cur_dst = None
        self.switch_selector(self.crystal_selector)
        self.switch_dst(self.first_selector())
        self.walker = RecipeWalker(self.recipe)

    def build_selectors(self, selector_list, vars):
        for var in vars:
            items = []
            selector = ItemSelector(self, items)
            if var.count.isdigit():
                count = int(var.count)
                selector.max_size = count
                selector.num_cols = min(10, count)
            selector.selecting = False
            selector.add_type(var.type)
            selector_list.append(selector)

    def switch_selector(self, selector):
        if self.cur_selector is not None:
            self.cur_selector.selecting = False
        self.cur_selector = selector
        self.cur_selector.selecting = True

    def switch_dst(self, selector):
        self.cur_dst = selector

    def first_selector(self):
        if len(self.input_selectors) > 0:
            return self.input_selectors[0]
        elif len(self.cost_selectors) > 0:
            return self.cost_selectors[0]
        else:
            return None

    def next_selector(self, selector):
        if selector == self.crystal_selector:
            return self.spell_selector
        elif selector == self.spell_selector:
            return self.first_selector()
        else:
            return self.next_dst(selector, True)

    def next_dst(self, selector, spells=False):
        if selector in self.input_selectors:
            index = self.input_selectors.index(selector)
            if index == len(self.input_selectors) - 1:
                if len(self.cost_selectors) > 0:
                    return self.cost_selectors[0]
                elif spells:
                    return self.crystal_selector
                else:
                    return self.first_selector()
            return self.input_selectors[index + 1]
        else:
            index = self.cost_selectors.index(selector)
            if index == len(self.cost_selectors) - 1:
                if spells:
                    return self.crystal_selector
                elif len(self.input_selectors) > 0:
                    return self.input_selectors[0]
                else:
                    return self.cost_selectors[0]
            return self.cost_selectors[index + 1]

    def exit(self):
        selectors = self.input_selectors + self.cost_selectors
        for selector in selectors:
            items = list(selector.items)
            for item in items:
                selector.remove_item(item)
                self.add_inventory(item)
        Window.exit(self)

    def add_inventory(self, item):
        dst = None
        if item.type == 'Crystal':
            dst = self.crystal_selector
        elif item.type == 'Spell':
            dst = self.spell_selector
        else:
            print 'Unknown item type: `' + item.type + '`'
            return False
        return dst.add_item(item, True)

    def key_released(self, key):
        Window.key_released(self, key)

        if key == pygame.K_s:
            self.switch_selector(self.next_selector(self.cur_selector))
        if key == pygame.K_d:
            self.switch_dst(self.next_dst(self.cur_dst))

        if key in Menu.select_keys:
            item = self.cur_selector.get_selection()
            if item is None:
                return
            success = False
            if self.cur_selector in self.input_selectors or \
               self.cur_selector in self.cost_selectors:
                success = self.add_inventory(item)
            elif self.cur_dst.is_allowed(item):
                success = self.cur_dst.add_item(item, True)
            else:
                return
            if not success:
                return
            self.cur_selector.remove_selection()

        if key == pygame.K_e:
            self.execute()

    def execute(self):
        variables = {}
        bindings = []
        bindings += zip(self.recipe.input, self.input_selectors)
        bindings += zip(self.recipe.cost, self.cost_selectors)
        for (var, selector) in bindings:
            if var.count.isdigit() and int(var.count) == 1:
                variables[var.name] = selector.items[0]
            else:
                variables[var.name] = selector.items
            if not var.count.isdigit():
                variables[var.count] = selector.num_items()
        
        if not self.walker.valid(variables, self.player):
            return
        self.walker.execute(variables, self.player)
        for var in self.recipe.output:
            print 'Looking up output variable ' + var.name
            item = variables[var.name]
            selector = None
            if var.type == 'Crystal':
                selector = self.crystal_selector
            else:
                selector = self.spell_selector
            if var.count.isdigit():
                selector.add_item(item)
            else:
                items = item
                for item in items:
                    selector.add_item(item)

        selectors = self.input_selectors + self.cost_selectors
        for selector in selectors:
            selector.clear()

    def display(self, dst):
        # draw the title
        label = self.recipe.label
        white = (255, 255, 255)
        red = (255, 0, 0)
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
            if selector == self.cur_selector:
                selector.draw_bounds(dst, white, corner, radius, 2)
            if selector == self.cur_dst:
                selector.draw_bounds(dst, red, corner, radius, 4)
            corner += selector_skip * selector.visible_rows()
