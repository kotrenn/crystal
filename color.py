class Color(object):
    def __init__(self, r, g, b):
        self.v = [r, g, b]

    # comparison operators
    def __eq__(self, c):
        return all([a == b for a, b in zip(self.v, c.v)])

    def __ne__(self, c):
        return any([a != b for a, b in zip(self.v, c.v)])

    def __lt__(self, c):
        return all([a < b for a, b in zip(self.v, c.v)])
        
    def __le__(self, c):
        return all([a <= b for a, b in zip(self.v, c.v)])
        
    def __gt__(self, c):
        return all([a > b for a, b in zip(self.v, c.v)])

    def __ge__(self, c):
        return all([a >= b for a, b in zip(self.v, c.v)])

    # indexed assignment
    def __setitem__(self, i, x):
        self.v[i] = x

    # indexed retrieval
    def __getitem__(self, i):
        return self.v[i]

    # get rgb tuple for rendering
    def tuple(self, val = 255):
        return tuple([x * val for x in self.v])

