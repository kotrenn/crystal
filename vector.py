import math

dims = 2

class vector(object):
    def __init__(self, *args):
        if len(args) == 0:
            self.v = [0, 0]
        elif len(args) == 1:
            v = args[0]
            self.v = list(v)
        elif len(args) == 2:
            x, y = args
            self.v = [x, y]

    # convert to string
    def __str__(self):
        return str(self.v)

    # vector equality
    def __eq__(self, v):
        return all([a == b for a, b in zip(self.v, v.v)])

    # vector addition
    def __add__(self, v):
        return vector([a + b for a, b in zip(self.v, v.v)])

    # vector subtraction
    def __sub__(self, v):
        return vector([a - b for a, b in zip(self.v, v.v)])

    # scalar multiplication
    def __mul__(self, s):
        return vector([x * s for x in self.v])

    def __rmul__(self, s):
        return vector([x * s for x in self.v])

    # scalar division
    def __div__(self, s):
        return vector([x / s for x in self.v])

    # dot product
    def __pow__(self, v):
        return sum([a * b for a, b in zip(self.v, v.v)])

    # internal product
    def __mod__(self, v):
        return vector([a * b for a, b in zip(self.v, v.v)])

    # compute the magnitude
    def mag(self):
        return math.sqrt(self ** self)

    # computed the normalized vector
    def norm(self):
        return self / self.mag()

    # compute a vector with y[i] = abs(x[i])
    def abs(self):
        return vector([abs(x) for x in self.v])

    # indexed assignment
    def __setitem__(self, i, x):
        self.v[i] = x

    # indexed retrieval
    def __getitem__(self, i):
        return self.v[i]

    # swap x and y coordinates
    def transpose(self):
        return vector(self.v[1], self.v[0])

    # convert to a list
    def list(self):
        return list(self.v)

    # convert to a tuple
    def tuple(self):
        return tuple(self.v)

    # rotate about the origin by angle theta (in degrees)
    def rotate(self, theta):
        x, y = self.v
        theta *= 2.0 * math.pi / 180.0
        self.v = [math.cos(theta) * x - math.sin(theta) * y,
                  math.sin(theta) * x + math.cos(theta) * y]
        return self
