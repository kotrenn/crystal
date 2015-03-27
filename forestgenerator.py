# Class for generating a simple forest for a level.  Currently surrounds the
# region in trees and draws simple stone paths between exits.

from level import *

class ForestGenerator(object):
    # Dummy code
    def __init__(self):
        x = 3

    # Build a level given parameters:
    #   level     - The Level object to populate
    #   vectors   - Unit length vectors in the direction of neighbors
    #   neighbors - Corresponding neighbors (matches up with vectors)
    # Assumes vectors are unit length
    def make_level(self, level, vectors, neighbors):
        dims = level.dims

        # Add tree border
        for row in range(dims[0]):
            level.grid.cells[row][0] = level.tiles['tree']
            level.grid.cells[row][dims[1] - 1] = level.tiles['tree']
        for col in range(dims[1]):
            level.grid.cells[0][col] = level.tiles['tree']
            level.grid.cells[dims[0] - 1][col] = level.tiles['tree']

        # Clear holes for neighboring locations
        for (vec, neighbor) in zip(vectors, neighbors):
            p = self.get_intersection(dims, vec)
            self.clear_tile(level, p)
            self.process_corner(level, p)

            # Add warp to neighbor with unknown location within the Level
            self.add_warp(level, neighbor, p)

        return level

    # Compute the intersection of a vector vec with the border of the Level.
    # Used for determining where to insert holes in the border for paths to
    # neighboring locations.
    def get_intersection(self, dims, vec):
        # Deal with transpose stuff for overworld coords -> level coords
        vec = vec.transpose()
        
        # Convert to unit coordinates
        w, h = map(float, (dims - vector(1, 1)).list())
        center = vector(w, h) / 2
        w2, h2 = center.list()
        new_vec = vector(vec.x / w2, vec.y / h2).norm()

        # Rotate 45 degrees
        rot_vec = vector(new_vec).rotate(-45)

        # Determine which quadrant we're in and compute the scaling ratio for
        # the unit square
        scale = None
        if rot_vec.x < 0: # north, west
            if rot_vec.y < 0: # north
                scale = -1 / new_vec.y
            else: # west
                scale = -1 / new_vec.x
        else: # south, east
            if rot_vec.y < 0: # east
                scale = 1 / new_vec.x
            else: # south
                scale = 1 / new_vec.y

        # Now compute the intersection point
        intersection = scale * new_vec

        # Convert back to original coordinates
        intersection %= center

        # Add in center
        intersection += center

        # Return coordinate of the tile to erase
        row, col = map(int, map(round, intersection.list()))
        return vector(row, col)

    # If we created a hole in a corner, then we need to clear out neighboring
    # trees so players can reach the corner.
    def process_corner(self, level, p):
        dims = level.dims
        
        # Initialize lots of helper variables
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

        # For each corner in the Level, if the current point matches up, clear
        # out the neighboring two cells.
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

    # Remove any trees from the given cell p
    def clear_tile(self, level, p):
        row, col = p.list()
        level.grid.cells[row][col] = level.tiles['blank']

    # Add in a Warp for movement between locations
    def add_warp(self, level, neighbor, p):
        dst = (neighbor, None)
        level.add_warp(p, dst)
