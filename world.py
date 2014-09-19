import math
import random

from forestgenerator import *
from vector import *

class World(object):
    def __init__(self, width, height):
        self.dims = vector(width, height)

        self.points = []
        self.edges = []

        #self.uniform(num_points)
        self.bridson(width / 12)

        self.edges = self.build_edges(self.euclid)

        self.generator = ForestGenerator()
        n = len(self.points)
        level_dims = vector(12, 17)
        self.levels = [Level(level_dims) for i in range(n)]
        for i in range(n):
            self.build_level(i)

        self.connect_levels()

    def out_of_bounds(self, p):
        return p.x < 0 or p.y < 0 or \
            p.x >= self.dims[0] or \
            p.y >= self.dims[1]

    def uniform(self, num_points):
        for _ in range(num_points):
            x = random.randint(0, self.dims[0] - 1)
            y = random.randint(0, self.dims[1] - 1)
            self.points.append(vector(x, y))

    def bridson(self, min_radius):
        # number of attempts per active point before being
        # marked as inactive
        max_samples = 30

        # pick a random start point
        start_x = random.randint(0, self.dims[0] - 1)
        start_y = random.randint(0, self.dims[1] - 1)
        start_point = vector(start_x, start_y)
        active = [start_point]
        points = []

        while len(active) > 0:
            cur = random.choice(active)
            found = False
            for _ in range(max_samples):
                # generate a new point in the annulus
                theta = 2.0 * math.pi * random.random()
                radius = min_radius * (1 + random.random())
                new_x = cur.x + radius * math.cos(theta)
                new_y = cur.y + radius * math.sin(theta)
                new_point = vector(new_x, new_y)

                # skip if it's out of bounds
                if self.out_of_bounds(new_point):
                    continue

                # check if it's too close to another point
                # replace later by a grid
                bound = min_radius ** 2
                too_close = False
                for p in points + active:
                    # skip current point
                    if p is cur:
                        continue

                    # compute distance^2
                    delta = p - new_point
                    dist = delta ** delta
                    if dist < bound:
                        too_close = True
                        break

                # go to the next point if too close
                # to an existing point
                if too_close:
                    continue

                # add to the active points
                found = True
                active.append(new_point)
                break

            # repeat if we did find a new point
            if found:
                continue

            # remove current point from active
            active.remove(cur)
            points.append(cur)

        # convert all points to integers
        for p in points:
            new_x = int(p.x)
            new_y = int(p.y)
            new_p = vector(new_x, new_y)
            self.points.append(new_p)

    def euclid(self, p, q):
        return (p - q) ** (p - q)

    def manhattan(self, p, q):
        delta = (p - q).abs()
        dx = delta.x
        dy = delta.y
        return max(dx, dy)

    def king(self, p, q):
        delta = (p - q).abs()
        dx = delta.x
        dy = delta.y
        return max(dx, dy)

    def build_edges(self, metric):
        # basic way to compute relative nearest neighbor
        ret = []
        n = len(self.points)
        print 'n = ' + str(n)
        for i in range(n):
            p_i = self.points[i]
            for j in range(i + 1, n):
                p_j = self.points[j]
                d_ij = metric(p_i, p_j)
                good = True
                for k in range(n):
                    if k == i or k == j:
                        continue
                    p_k = self.points[k]
                    d_ik = metric(p_i, p_k)
                    d_jk = metric(p_j, p_k)
                    max_d = max(d_ik, d_jk)
                    if max_d < d_ij:
                        good = False
                        break
                if not good:
                    continue
                ret.append((i, j))
        return ret

    def neighbors(self, i):
        ret = []
        for (u, v) in self.edges:
            if u == i:
                ret.append(v)
            elif v == i:
                ret.append(u)
        return ret

    def build_level(self, i):
        level = self.levels[i]
        p = self.points[i]
        neighbors = self.neighbors(i)
        vectors = []
        for j in neighbors:
            q = self.points[j]
            delta = (q - p).norm()
            vectors.append(delta)
        neighbors = [self.levels[v] for v in neighbors]
        return self.generator.make_level(level, vectors, neighbors)

    def connect_levels(self):
        for (i, j) in self.edges:
            self.add_warp(i, j)
            self.add_warp(j, i)

    def add_warp(self, i, j):
        level_i = self.levels[i]
        level_j = self.levels[j]
        warps_i = level_i.warps
        warps_j = level_j.warps
        the_neighbor = None

        new_i = []
        for (src, dst) in warps_i:
            level, loc = dst
            if level is level_j:
                continue
            new_i.append((src, dst))

        for (src, dst) in warps_j:
            neighbor, loc = dst
            if neighbor is not level_i:
                continue

            new_src = None
            for (src_i, dst_i) in warps_i:
                if dst_i[0] is level_j:
                    new_src = src_i
                    break
            new_dst = (level_j, src)
            new_i.append((new_src, new_dst))

        level_i.warps = new_i
