from level import *

class ForestGenerator(object):
    def __init__(self):
        x = 3

    # assumes vectors are unit length
    def make_level(self, vectors):
        dims = vector(12, 17)
        level = Level(dims)

        # add tree border
        for row in range(dims[0]):
            level.grid.cells[row][0] = level.tiles['tree']
            level.grid.cells[row][dims[1] - 1] = level.tiles['tree']
        for col in range(dims[1]):
            level.grid.cells[0][col] = level.tiles['tree']
            level.grid.cells[dims[0] - 1][col] = level.tiles['tree']

        # clear holes for neighboring locations
        for vec in vectors:
            p = self.get_intersection(dims, vec)
            self.clear_tile(level, p)
            self.process_corner(level, p)

        return level

    def get_intersection(self, dims, vec):
        # deal with transpose stuff for
        # real world -> level coords
        vec = vec.transpose()
        
        # convert to unit coordinates
        w, h = map(float, (dims - vector(1, 1)).list())
        center = vector(w, h) / 2
        w2, h2 = center.list()
        new_vec = vector(vec.x / w2, vec.y / h2).norm()

        # rotate 45 degrees
        rot_vec = vector(new_vec).rotate(-45)

        # determine which quadrant we're in
        # and compute the scaling ratio for
        # the unit square
        scale = None
        if rot_vec.x < 0: #north, west
            if rot_vec.y < 0: # north
                scale = -1 / new_vec.y
            else: # west
                scale = -1 / new_vec.x
        else: # south, east
            if rot_vec.y < 0: # east
                scale = 1 / new_vec.x
            else: # south
                scale = 1 / new_vec.y

        # now compute the intersection point
        intersection = scale * new_vec

        # convert back to original coordinates
        intersection %= center

        # add in center
        intersection += center

        # return tile coord
        row, col = map(int, map(round, intersection.list()))
        return vector(row, col)

    def process_corner(self, level, p):
        dims = level.dims
        x0 = y0 = 0
        x1 = dims[0] - 1
        y1 = dims[1] - 1
        tl = vector(x0, y0)
        tr = vector(x1, y0)
        bl = vector(x0, y1)
        br = vector(x1, y1)

        up = vector(0, -1)
        down = vector(0, 1)
        left = vector(-1, 0)
        right = vector(1, 0)

        if p == tl:
            self.clear_tile(level, tl + right)
            self.clear_tile(level, tl + down)
        elif p == tr:
            self.clear_tile(level, tr + left)
            self.clear_tile(level, tr + down)
        elif p == bl:
            self.clear_tile(level, bl + right)
            self.clear_tile(level, bl + up)
        elif p == br:
            self.clear_tile(level, br + left)
            self.clear_tile(level, br + up)

    def clear_tile(self, level, p):
        row, col = p.list()
        level.grid.cells[row][col] = level.tiles['blank']
