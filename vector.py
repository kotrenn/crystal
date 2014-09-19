import math

dims = 2

class vector(object):
    def __init__(self, *args):
        if len(args) == 0:
            self.x = self.y = 0
        elif len(args) == 1:
            v = args[0]
            self.x = v[0]
            self.y = v[1]
        elif len(args) == 2:
            self.x, self.y = args

    # convert to string
    def __str__(self):
        return '[' + str(self.x) + ', ' + str(self.y) + ']'

    # vector equality
    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    # vector addition
    def __add__(self, v):
        return vector(self.x + v.x, self.y + v.y)

    # vector subtraction
    def __sub__(self, v):
        return vector(self.x - v.x, self.y - v.y)

    # scalar multiplication
    def __mul__(self, s):
        return vector(self.x * s, self.y * s)

    def __rmul__(self, s):
        return vector(self.x * s, self.y * s)

    # scalar division
    def __div__(self, s):
        return vector(self.x / s, self.y / s)

    # dot product
    def __pow__(self, v):
        return self.x * v.x + self.y * v.y

    # internal product
    def __mod__(self, v):
        return vector(self.x * v.x, self.y * v.y)

    # compute the magnitude
    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    # computed the normalized vector
    def norm(self):
        return self / self.mag()

    # compute a vector with y[i] = abs(x[i])
    def abs(self):
        return vector(abs(self.x), abs(self.y))

    # indexed assignment
    def __setitem__(self, i, val):
        if i == 0:
            self.x = val
        else:
            self.y = val

    # indexed retrieval
    def __getitem__(self, i):
        if i == 0:
            return self.x
        else:
            return self.y

    # swap x and y coordinates
    def transpose(self):
        return vector(self.y, self.x)

    # convert to a list
    def list(self):
        return [self.x, self.y]

    # convert to a tuple
    def tuple(self):
        return (self.x, self.y)

    # rotate about the origin by angle theta (in degrees)
    def rotate(self, theta):
        x, y = self.x, self.y
        theta *= math.pi / 180.0
        self.x = math.cos(theta) * x - math.sin(theta) * y
        self.y = math.sin(theta) * x + math.cos(theta) * y
        return self
