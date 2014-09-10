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
        ret += '  req = ' + str(map(str, self.req)) + '\n'
        ret += '  code = {\n'
        for stat in self.code:
            ret += '    ' + str(stat) + '\n'
        ret += '  }'
        return ret
