import math

dims = 2

class vector(object):
    def __init__(self, *args):
        if len(args) == 0:
            self.v = [0] * dims
        elif len(args) == 1:
            v = args[0]
            self.v = list(v)
        elif len(args) == 2:
            x, y = args
            self.v = [x, y]
            

    def __str__(self):
        return str(self.v)

    def __eq__(self, v):
        return all([a == b for a, b in zip(self.v, v.v)])

    def __add__(self, v):
        return vector([a + b for a, b in zip(self.v, v.v)])

    def __sub__(self, v):
        return vector([a - b for a, b in zip(self.v, v.v)])

    def __mul__(self, s):
        return vector([x * s for x in self.v])

    def __rmul__(self, s):
        return vector([x * s for x in self.v])

    def __div__(self, s):
        return vector([x / s for x in self.v])

    def __pow__(self, v):
        return sum([a * b for a, b in zip(self.v, v.v)])

    def __mod__(self, v):
        return vector([a * b for a, b in zip(self.v, v.v)])

    def mag(self):
        return math.sqrt(self ** self)

    def norm(self):
        return self / self.mag()

    def abs(self):
        return vector([abs(x) for x in self.v])

    def __setitem__(self, i, x):
        self.v[i] = x

    def __getitem__(self, i):
        return self.v[i]

    def list(self):
        return list(self.v)

    def rotate(self, theta):
        x, y = self.v
        theta *= 2.0 * math.pi / 180.0
        self.v = [math.cos(theta) * x - math.sin(theta) * y,
                  math.sin(theta) * x + math.cos(theta) * y]
        return self
