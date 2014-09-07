class Recipe(object):
    def __init__(self, name):
        self.name = name
        self.label = '[Undefined Label (' + self.name + ')]'
        self.cost = []
        self.input = []
        self.output = []
        self.req = []
        self.code = []

    def __str__(self):
        ret = ''
        ret += 'Recipe ' + self.name + ':\n'
        ret += '  label = `' + self.label + '`\n'
        ret += '  cost = ' + str(map(str, self.cost)) + '\n'
        ret += '  input = ' + str(map(str, self.input)) + '\n'
        ret += '  output = ' + str(map(str, self.output)) + '\n'
        ret += '  req = ' + str(self.req) + '\n'
        ret += '  code = ' + str(self.code) + '\n'
        return ret

class Variable(object):
    def __init__(self):
        self.type = ''
        self.name = ''
        self.count = 1
        
    def __str__(self):
        ret = self.name + ':' + self.type + 'x' + str(self.count)
        return ret

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
        print 'token = ' + token
        if token == 'label':
            cur_recipe.label = self.read_label()
        elif token == 'cost':
            self.read_variables(cur_recipe.cost)
        elif token == 'input':
            self.read_variables(cur_recipe.input)
        elif token == 'output':
            self.read_variables(cur_recipe.output)
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
            print 'var token = ' + token
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
