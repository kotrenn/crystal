import random

from crystalfactory import *
from recipeparser import *
from spell import *

class RecipeWalker(object):
    def __init__(self, recipe):
        self.recipe = recipe
        self.factory = BasicCrystalFactory()

    def valid(self, variables, player):
        for statement in self.recipe.req:
            if not self.eval_func(statement.func, variables, player):
                return False
        return True

    def execute(self, variables, player):
        for statement in self.recipe.code:
            self.eval_statement(statement, variables, player)

    def eval_statement(self, statement, variables, player):
        result = self.eval(statement.func, variables, player)
        if statement.var is not None:
            self.assign_var(variables, statement.var, result)
        return result

    def get_method(self, func_name):
        func_name = func_name[1:] # get rid of `@`
        mapping = {
            'random_pipes': (1, self.func_random_pipes),
            'random_color': (0, self.func_random_color),
            'sum': (2, self.func_sum),
            'min': (1, self.func_min),
            'add': (2, self.func_add),
            'sub': (2, self.func_sub),
            'divide': (2, self.func_divide),
            'eq': (2, self.func_eq),
            'lt': (2, self.func_lt),
            'leq': (2, self.func_leq),
            'geq': (2, self.func_geq),
            'randint': (2, self.func_randint),
            'Color': (3, self.func_color),
            'Spell': (1, self.func_spell),
            'add_hp': (1, self.func_add_hp),
            'add_mana': (1, self.func_add_mana),
            'add_mana_gen': (1, self.func_add_mana_gen),
            'add_corruption': (2, self.func_add_corruption),
            'has_corruption': (1, self.func_has_corruption),
            'remove_corruption': (1, self.func_remove_corruption),
            'spell_crystals': (1, self.func_spell_crystals),
            'random_attribute': (1, self.func_random_attribute),
            'get_att': (2, self.func_get_att),
            'set_att': (3, self.func_set_att)
            }
        if func_name in mapping:
            return mapping[func_name]
        else:
            print 'Error: Unknown function `@' + func_name + '`'
            return None

    def eval(self, val, variables, player):
        classes = str(type.mro(type(val)))
        if 'str' in classes:
            if val.isdigit():
                return self.eval_constant(val)
            return self.eval_variable(val, variables, player)
        elif 'FunctionCall' in classes:
            return self.eval_func(val, variables, player)
        else:
            return val

    def eval_constant(self, val):
        return int(val)

    def eval_variable(self, var_name, variables, player):
        code = ''
        if '.' in var_name:
            root_name = var_name.split('.')[0]
            if root_name not in variables:
                print 'Error: Unknown variable `' + root_name + '`'
                return None
            code = 'variables[\'' + root_name + '\'].'
            code += ''.join(var_name.split('.')[1:])
        elif '$' in var_name:
            root_name = var_name.split('$')[0]
            if root_name not in variables:
                print 'Error: Unknown variable `' + root_name + '`'
                return None
            code = 'variables[\'' + root_name + '\']'
            val = ''.join(var_name.split('$')[1:])
            code = '[x.' + val + ' for x in ' + code + ']'
        else:
            code = 'variables[\'' + var_name + '\']'
        result = None
        code = 'result = ' + code
        print 'Generated code (eval): `' + code + '`'
        exec code
        return result

    def eval_func(self, func, variables, player):
        name = func.name
        args = [self.eval(x, variables, player) for x in func.args]
        arg_count, foo = self.get_method(name)
        if len(args) != arg_count:
            print 'Error: Incorrect number of arguments for function `' + \
                name + '`;  expected ' + str(arg_count) + ', got ' + \
                str(len(args))
            return None
        return foo(args, variables, player)

    def get_var(self, var_name, variables):
        if var_name not in variables:
            print 'Error: Unknown variable `' + var_name + '`'
            return
        return variables[var_name]

    def assign_var(self, variables, var_name, val):
        code = 'None'
        if '.' in var_name:
            root_name = var_name.split('.')[0]
            if root_name not in variables:
                print 'Error: Unknown variable `' + root_name + '`'
                return None
            code = 'variables[\'' + root_name + '\'].'
            code += ''.join(var_name.split('.')[1:])
        elif '$' in var_name:
            print 'Unsupported: Vector assignment'
            return None
        else:
            code = 'variables[\'' + var_name + '\']'
        code = code + ' = val'
        print 'Generated code: `' + code + '`'
        exec code

    def func_random_pipes(self, args, variables, player):
        print 'func_random_pipes()'
        pipes = args[0]
        num_in = pipes.count('In')
        num_out = pipes.count('Out')
        new_pipes = self.factory.random_pipes(num_in, num_out)
        print 'new_pipes = ' + str(new_pipes)
        return new_pipes

    def func_random_color(self, args, variables, player):
        color = Color(False, False, False)
        color[random.randint(0, 2)] = True
        if random.randint(1, 5) == 1:
            color[random.randint(0, 2)] = True
        if random.randint(1, 50) == 1:
            color = Color(True, True, True)
        return color

    def func_sum(self, args, variables, player):
        return sum(args[0], args[1])

    def func_min(self, args, variables, player):
        return min(args[0])

    def func_add(self, args, variables, player):
        lhs = args[0]
        rhs = args[1]
        return lhs + rhs
    
    def func_sub(self, args, variables, player):
        lhs = args[0]
        rhs = args[1]
        return lhs - rhs
    
    def func_divide(self, args, variables, player):
        lhs = args[0]
        rhs = args[1]
        return lhs / rhs

    def func_eq(self, args, variables, player):
        lhs = args[0]
        rhs = args[1]
        return lhs == rhs

    def func_lt(self, args, variables, player):
        lhs = args[0]
        rhs = args[1]
        return lhs < rhs

    def func_leq(self, args, variables, player):
        lhs = args[0]
        rhs = args[1]
        return lhs <= rhs

    def func_geq(self, args, variables, player):
        lhs = args[0]
        rhs = args[1]
        return lhs >= rhs

    def func_randint(self, args, variables, player):
        a = args[0]
        b = args[1]
        return random.randint(a, b)

    def func_color(self, args, variables, player):
        r = args[0]
        g = args[1]
        b = args[2]
        return Color(r, g, b)

    def func_spell(self, args, variables, player):
        size = args[0]
        spell = Spell(player, size)
        return spell

    def func_add_hp(self, args, variables, player):
        hp_gain = args[0]
        hp = player.hp
        hp.max_val += hp_gain
        hp.add(hp_gain)

    def func_add_mana(self, args, variables, player):
        delta = args[0]
        for i in range(3):
            mana = player.mana[i]
            mana.max_val += delta[i]
            mana.add(delta[i])

    def func_add_mana_gen(self, args, variables, player):
        delta = args[0]
        player.mana_gen += delta

    def func_add_corruption(self, args, variables, player):
        spell = args[0]
        amount = args[1]
        if random.randint(1, 5) == 1 and False:
            amount += random.choice([-1, 1])
        for _ in range(amount):
            crystal = Crystal()
            crystal.color = Color(0.5, 0.5, 0.5)
            crystal.pipes = [None] * 6
            crystal.atts['Movable'] = False
            crystal.atts['Corruption'] = True

            row, col = -1, -1
            grid = spell.grid
            while row < 0 or col < 0:
                row = random.randint(0, grid.num_rows() - 1)
                col = random.randint(0, grid.num_cols(row) - 1)
                if spell.grid.cells[row][col] is not None:
                    row, col = -1, -1
            spell.grid.cells[row][col] = crystal
        return spell

    def func_has_corruption(self, args, variables, player):
        spell = args[0]
        grid = spell.grid
        for row in range(grid.num_rows()):
            for col in range(grid.num_cols(row)):
                crystal = grid.cells[row][col]
                if crystal is None:
                    continue
                if 'Corruption' not in crystal.atts:
                    continue
                if not crystal.atts['Corruption']:
                    continue
                return True
        return False

    def func_remove_corruption(self, args, variables, player):
        spell = args[0]
        grid = spell.grid
        corrupt = []
        for row in range(grid.num_rows()):
            for col in range(grid.num_cols(row)):
                crystal = grid.cells[row][col]
                if crystal is None:
                    continue
                if 'Corruption' not in crystal.atts:
                    continue
                if not crystal.atts['Corruption']:
                    continue
                corrupt.append((row, col))
        if len(corrupt) == 0:
            return
        row, col = random.choice(corrupt)
        grid.cells[row][col] = None

    def func_spell_crystals(self, args, variables, player):
        spell = args[0]
        grid = spell.grid
        ret = []
        for row in range(grid.num_rows()):
            for col in range(grid.num_cols(row)):
                crystal = grid.cells[row][col]
                if crystal is not None:
                    if crystal.atts['Movable']:
                        ret.append(crystal)
        return ret

    def func_random_attribute(self, args, variables, player):
        atts = args[0]
        elements = ['Neutral', 'Fire', 'Ice', 'Heal', 'Lightning']
        available = [att for att in atts if att in elements]
        if len(available) == 0:
            return random.choice(elements)
        return random.choice(available)

    def func_get_att(self, args, variables, player):
        atts = args[0]
        att = args[1]
        return atts[att]

    def func_set_att(self, args, variables, player):
        atts = args[0]
        att = args[1]
        val = args[2]
        atts[att] = val
