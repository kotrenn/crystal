class Statement(object):
    def __init__(self):
        self.var = None
        self.func = None

    def __str__(self):
        ret = ''
        if self.var:
            ret += self.var + ' = '
        ret += str(self.func)
        return ret
