class Variable(object):
    def __init__(self):
        self.type = ''
        self.name = ''
        self.count = '1'
        
    def __str__(self):
        ret = self.name + ':' + self.type + 'x' + str(self.count)
        return ret
