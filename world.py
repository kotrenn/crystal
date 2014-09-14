import random

from vector import *

class World(object):
    def __init__(self, width, height, num_points):
        self.dims = [width, height]

        self.points = []
        self.edges = []
        for _ in range(num_points):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            self.points.append(vector(x, y))

        # basic way to compute relative nearest neighbor
        n = num_points
        for i in range(n):
            p_i = self.points[i]
            for j in range(i + 1, n):
                p_j = self.points[j]
                v_ij = p_i - p_j
                d_ij = v_ij ** v_ij
                good = True
                for k in range(1, n):
                    if k == i or k == j:
                        continue
                    p_k = self.points[k]
                    v_ik = p_i - p_k
                    v_jk = p_j - p_k
                    d_ik = v_ik ** v_ik
                    d_jk = v_jk ** v_jk
                    max_d = max(d_ik, d_jk)
                    if max_d < d_ij:
                        good = False
                        break
                if not good:
                    continue
                self.edges.append((i, j))
