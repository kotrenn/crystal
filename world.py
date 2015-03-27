# World class, which keeps track of the overworld and the levels contained within.  Provides
# implementation for the generation of the overworld along with subsequent generation of each level
# level within.

import math
import random

from forestgenerator import *
from vector import *

class World(object):
    def __init__(self, width, height):
        self.dims = vector(width, height)

        self.points = []   # List of where each location is in the world
        self.edges = []    # List of which pairs of locations are connected

        # Begin world generation by selecting points in a rectangular region
        print 'Generating nodes...'
        #self.uniform(num_points)
        self.bridson(width / 12)

        # Now we want to connect up some of the points (add roads between locations)
        n = len(self.points)
        print 'Connecting ' + str(n) + ' nodes...'
        self.edges = self.build_edges(self.euclid)

        # Place some actual trees and content within each of the locations
        self.generator = ForestGenerator()
        level_dims = vector(12, 17)
        print 'Building levels...'
        self.levels = [Level(level_dims) for i in range(n)]
        for i in range(n):
            self.build_level(i)

        # Add in connections so that when players reach the edge of a location they
        # will be taken to the corresponding location
        print 'Connecting levels...'
        self.connect_levels()
        print 'World generation done!'

        # Check if a point is within rectangular bounds
    def out_of_bounds(self, p):
        return p.x < 0 or p.y < 0 or \
            p.x >= self.dims[0] or \
            p.y >= self.dims[1]

        # Simple uniform distribution for selecting points to use as locations
        # during world generation
    def uniform(self, num_points):
        for _ in range(num_points):
            x = random.randint(0, self.dims[0] - 1)
            y = random.randint(0, self.dims[1] - 1)
            self.points.append(vector(x, y))

        # Fancier distribution for selecting points to use as locations during
        # world generation.  This uses Bridson's algorithm for Poisson-disc
        # sampling, which creates a much more even spread than a pure uniform
        # distribution would.  A good summary of the process can be found at
        # http://bost.ocks.org/mike/algorithms/
    def bridson(self, min_radius):
        # Number of attempts per active point before being marked as inactive
        max_samples = 30

        # Pick a random start point
        start_x = random.randint(0, self.dims[0] - 1)
        start_y = random.randint(0, self.dims[1] - 1)
        start_point = vector(start_x, start_y)
        active = [start_point]
        points = []

        # Keep going while there are still places we can extend from
        while len(active) > 0:
            # Pick a point at random from the currently active points
            cur = random.choice(active)
            found = False
            for _ in range(max_samples):
                # Generate a new point in the annulus of cur
                theta = 2.0 * math.pi * random.random()
                radius = min_radius * (1 + random.random())
                new_x = cur.x + radius * math.cos(theta)
                new_y = cur.y + radius * math.sin(theta)
                new_point = vector(new_x, new_y)

                # Skip if it's out of bounds
                if self.out_of_bounds(new_point):
                    continue

                # Check to see if it's too close to another point
                # TODO: replace later by a grid to improve lookup performance
                bound = min_radius ** 2
                too_close = False
                for p in points + active:
                    # skip current point
                    if p is cur:
                        continue

                    # Compute distance^2
                    delta = p - new_point
                    dist = delta ** delta
                    if dist < bound:
                        too_close = True
                        break

                # Go to the next point if too close to an existing point
                if too_close:
                    continue

                # Add the new point to the active points
                found = True
                active.append(new_point)
                break

            # Repeat if we did find a new point
            if found:
                continue

            # Remove current point from the active set
            active.remove(cur)
            points.append(cur)

        # Convert all points from floats to integers
        for p in points:
            new_x = int(p.x)
            new_y = int(p.y)
            new_p = vector(new_x, new_y)
            self.points.append(new_p)

    # Euclidean distance metric
    def euclid(self, p, q):
        return (p - q) ** (p - q)

    # Manhattan distance metric
    def manhattan(self, p, q):
        delta = (p - q).abs()
        dx = delta.x
        dy = delta.y
        return max(dx, dy)

    # Distance metric based on king moves in chess
    def king(self, p, q):
        delta = (p - q).abs()
        dx = delta.x
        dy = delta.y
        return max(dx, dy)

    # Connect locations together based on the Relative Nearest Neighbor, which has an edge
    # between two nodes i and j if and only if there are no extra points k in the intersection
    # of the bounding circles of both i and j.
    #
    # http://www.passagesoftware.net/webhelp/Introduction.htm#Relative_Neighborhood_Network.htm
    #
    # We also take as input a function metric to use as a distance metric.  Different metrics
    # lead to different resulting networks.  Switching them around can lead to different resulting
    # aesthetics.  Current metrics provided:  Euclidean, Manhattan, Chess King
    def build_edges(self, metric):
        # For now, we iterate over every possible edge and check to see if the neighbor conditions
        # are met by comparing against all other points.  Slow O(n^3) algorithm.
        # TODO: look up algorithms for improving this;  test performance
        ret = []
        n = len(self.points)
        for i in range(n):
            p_i = self.points[i]
            for j in range(i + 1, n):
                p_j = self.points[j]
                d_ij = metric(p_i, p_j)
                good = True
                for k in range(n):
                    if k == i or k == j:
                        continue
                    
                    # Now actually test the neighbor condition
                    p_k = self.points[k]
                    d_ik = metric(p_i, p_k)
                    d_jk = metric(p_j, p_k)
                    max_d = max(d_ik, d_jk)
                    if max_d < d_ij:
                        good = False
                        break
                
                # Move on if a point breaks the condition
                if not good:
                    continue
                ret.append((i, j))
        return ret

    # Get a list of all directly adjacent locations for a given location i
    def neighbors(self, i):
        ret = []
        for (u, v) in self.edges:
            if u == i:
                ret.append(v)
            elif v == i:
                ret.append(u)
        return ret

    # For each location, fill in the trees and passages.  We also build up a
    # list of neighbors so that the level generator can add openings for players
    # to walk to neighboring locations.
    def build_level(self, i):
        level = self.levels[i]
        p = self.points[i]
        neighbors = self.neighbors(i)
        
        # Provide vectors so we can compute slope and make slightly more accurate openings
        vectors = []
        for j in neighbors:
            q = self.points[j]
            delta = (q - p).norm()
            vectors.append(delta)
        neighbors = [self.levels[v] for v in neighbors]
        
        # Have the current level generator make the actual level for us
        return self.generator.make_level(level, vectors, neighbors)

    # Add in connections between locations
    def connect_levels(self):
        for (i, j) in self.edges:
            self.add_warp(i, j)
            self.add_warp(j, i)

    # Add in the actual "physical" connection from location i to j.
    # When players walk onto a "warp", they will be immediately taken to
    # another location in the game.  We use this to act as a method for
    # players to move from one location to another at the borders.  Warps
    # are currently stored as tuples within tuples.
    # TODO: Expand to general Warp class for bookkeeping and general usability
    def add_warp(self, i, j):
        level_i = self.levels[i]
        level_j = self.levels[j]
        warps_i = level_i.warps
        warps_j = level_j.warps
        the_neighbor = None

    # Build up new_i as all current warps from i *excluding* any to j
        new_i = []
        for (src, dst) in warps_i:
            level, loc = dst
            if level is level_j:
                continue
            new_i.append((src, dst))

    # Search for the warp information within the warps associated with j
        for (src, dst) in warps_j:
            neighbor, loc = dst
            if neighbor is not level_i:
                continue

            new_src = None
            for (src_i, dst_i) in warps_i:
                if dst_i[0] is level_j:
                    new_src = src_i
                    break
                
            # Build and add the actual warp
            new_dst = (level_j, src)
            new_i.append((new_src, new_dst))

        # Update the i warps with our new addition
        level_i.warps = new_i
