from crystalfactory import *
from recipeparser import *

class RecipeWalker(object):
    def __init__(self, recipe):
        self.recipe = recipe
        self.factory = BasicCrystalFactory()

    def valid(self, variables, player):
        for req in self.recipe.req:
            if not self.eval_func(req, variables, player):
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
            'random_pipes': (1, self.func_random_pipes)
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
            print 'Unsupported: Vector member access'
            return None
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
