from functioncall import *
from recipe import *
from statement import *
from variable import *

class RecipeParser(object):
    def __init__(self):
        self.file = None
        self.prev_x = ''

    def open(self, filename):
        self.file = open(filename, 'r')

    def close(self):
        self.file.close()

    def read(self):
        ret = []
        cur_recipe = None
        token = self.next_token()
        while token:
            if token[-1] == ':':
                name = token[:-1]
                cur_recipe = Recipe(name)
                print 'Found new recipe `' + name + '`'
                ret.append(cur_recipe)
            else:
                self.process_token(token, cur_recipe)
            token = self.next_token()
        return ret

    def next_token(self, break_newline=False):
        ret = ''
        #x = self.file.read(1)
        x = self.prev_x
        if not x:
            x = self.file.read(1)
        while x and x.isspace(): # munch whitespace
            if break_newline and x == '\n':
                return ret
            x = self.file.read(1)
        while x and not x.isspace():
            if break_newline and x == '\n':
                return ret
            ret += x
            x = self.file.read(1)
        self.prev_x = x
        return ret

    def process_token(self, token, cur_recipe):
        if token == 'label':
            cur_recipe.label = self.read_label()
        elif token == 'cost':
            self.read_variables(cur_recipe.cost)
        elif token == 'input':
            self.read_variables(cur_recipe.input)
        elif token == 'output':
            self.read_variables(cur_recipe.output)
        elif token == 'req':
            self.read_code(cur_recipe.req)
        elif token == 'code':
            self.read_code(cur_recipe.code)
        else:
            print 'Unknown token: ' + token

    def read_label(self):
        ret = ''
        
        # get to a quote
        x = ''
        while x != '"':
            x = self.file.read(1)

        # read in the string
        escape = {
            '\\': '\\',
            'n': '\n',
            't': '\t',
            '\"': '\"',
            '\'': '\''
            }
        x = ''
        while x != '"':
            x = self.file.read(1)
            if x == '\\':
                y = self.file.read(1)
                if y in escape:
                    ret += escape[y]
                else:
                    ret += y
                x = ''
            elif x != '"':
                ret += x
                
        return ret
    
    def read_variables(self, dst):
        cur_variable = None
        token = self.next_token(True)
        while token:
            if token[0] == ':':
                type = token[1:]
                cur_variable = Variable()
                cur_variable.type = type
                dst.append(cur_variable)
            elif token[0] == 'x':
                count = token[1:]
                cur_variable.count = count
            else:
                cur_variable.name = token
            token = self.next_token(True)

    def read_code(self, dst):
        token = self.next_token(True) # munch '{'
        if token != '{':
            print 'Error: missing {'
        token = self.next_token()
        cur_statement = None
        while token:
            if token == '}':
                break
            cur_statement = Statement()
            dst.append(cur_statement)
            if token[0] != '@':
                cur_statement.var = token
                token = self.next_token() # munch '='
                token = self.next_token() # get function name
            if self.prev_x != '\n':
                token += self.file.readline()
            code_line = ''.join(token.split())
            func = FunctionCall(code_line)
            cur_statement.func = func
            token = self.next_token()
