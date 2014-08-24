import pygame
import random

from monster import *
from squaregrid import *
from vector import *

class World(object):
    def __init__(self):
        self.dims = vector(12, 17)
        self.tiles = {
            'blank': [0, 8],
            'tree': [0, 9]
        }
        self.tiles = {k: vector(v) for (k, v) in self.tiles.iteritems()}
        self.grid = SquareGrid(self.dims)

        for row in range(self.dims[0]):
            for col in range(self.dims[1]):
                if random.randint(1, 10) == 1:
                    self.grid.cells[row][col] = self.tiles['tree']
                else:
                    self.grid.cells[row][col] = self.tiles['blank']

        self.actors = [Monster(self) for _ in range(5)]

    def is_blocked(self, loc):
        if self.grid.out_of_bounds(loc):
            return True
        row = loc[0]
        col = loc[1]
        walls = ['tree']
        tile = self.grid.cells[row][col]
        for wall in walls:
            if self.tiles[wall] == tile:
                return True
        return False

    class Node(object):
        FLOOR_COST = 10
        STRAIGHT_COST = 9
        
        def __init__(self, loc, source_dir, cost, heuristic):
            self.loc = vector(loc)
            self.dir = source_dir
            self.cost = cost
            self.heuristic = heuristic

        def total(self):
            return self.cost + self.heuristic

        def __str__(self):
            ret = 'Node:'
            ret += ' loc: ' + str(self.loc)
            ret += ' dir: ' + str(self.dir)
            ret += ' cost: ' + str(self.cost)
            ret += ' heur: ' + str(self.heuristic)
            return ret

    def heuristic(self, loc, dst):
        offset = (dst - loc).abs()
        num_diagonal = min(offset.list())
        num_straight = max(offset.list()) - num_diagonal
        nums = vector(num_diagonal, num_straight)
        costs = vector(World.Node.FLOOR_COST,
                       World.Node.STRAIGHT_COST)
        return nums ** costs

    def a_star(self, src, dst):
        # currently just dijkstra's b/c zero heuristic
        grid = self.grid
        dirs = [DIR_NW, DIR_N, DIR_NE, DIR_E,
                DIR_SE, DIR_S, DIR_SW, DIR_W]
        q = [World.Node(src, DIR_NONE, 0,
                        self.heuristic(src, dst))]
        ret = DIR_NONE
        finished = []
        while len(q) > 0 and ret == DIR_NONE:
            # find the minimum cost node
            cur = None
            off = -1
            for (i, node) in enumerate(q):
                closer = False
                if cur is None:
                    closer = True
                elif cur.total() > node.total():
                    closer = True
                if closer:
                    cur = node
                    off = i
            q.pop(off)

            # check if we've reached the goal
            if cur.loc == dst:
                ret = cur.dir
                continue

            # check if already visited
            if cur.loc.list() in finished:
                continue
            
            finished.append(cur.loc.list())

            # get neighbors
            neighbors = []
            for dir in dirs:
                new_loc = grid.move_loc(dir, cur.loc)
                if grid.out_of_bounds(new_loc):
                    continue
                if self.is_blocked(new_loc):
                    continue

                # inherit parent direction if possible
                new_dir = cur.dir
                if new_dir == DIR_NONE:
                    new_dir = dir
                # compute the cost of moving to this node
                move_cost = World.Node.FLOOR_COST
                
                new_cost = cur.cost + move_cost
                new_node = World.Node(new_loc, new_dir, new_cost,
                                      self.heuristic(new_loc, dst))
                q.append(new_node)

        return ret
