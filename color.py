class Color(object):
    def __init__(self, *args):
        if len(args) == 0:
            self.v = [0, 0, 0]
        elif len(args) == 1:
            v = args[0]
            self.v = list(v)
        elif len(args) == 3:
            r, g, b = args
            self.v = [r, g, b]

    # string output
    def __str__(self):
        return str(self.tuple(1))

    # comparison operators
    def __eq__(self, c):
        if isinstance(c, (int, long)):
            if c == 0:
                return all([x == 0 for x in self.v])
            return False
        if isinstance(c, (Color)):
            return all([a == b for a, b in zip(self.v, c.v)])
        return False

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

        
    # arithmetic
    
    # vector addition
    def __add__(self, c):
        return Color([a + b for a, b in zip(self.v, c.v)])

    # vector subtraction
    def __sub__(self, c):
        return Color([a - b for a, b in zip(self.v, c.v)])

    # scalar multiplication
    def __mul__(self, s):
        return Color([x * s for x in self.v])

    def __rmul__(self, s):
        return Color([x * s for x in self.v])

    # scalar division
    def __div__(self, s):
        return Color([x / s for x in self.v])

    
    # indexed assignment
    def __setitem__(self, i, x):
        self.v[i] = x

    # indexed retrieval
    def __getitem__(self, i):
        return self.v[i]

    # get rgb tuple for rendering
    def tuple(self, val = 255):
        return tuple([x * val for x in self.v])

