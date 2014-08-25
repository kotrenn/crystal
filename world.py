import bisect
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
                if random.randint(1, 10) <= 3:
                    self.grid.cells[row][col] = self.tiles['tree']
                else:
                    self.grid.cells[row][col] = self.tiles['blank']

        for row in range(self.dims[0]):
            self.grid.cells[row][0] = self.tiles['blank']
            self.grid.cells[row][1] = self.tiles['tree']
        self.grid.cells[self.dims[0] - 1][1] = self.tiles['blank']

        self.actors = []
        self.actors = [Monster(self) for _ in range(5)]
        self.player = None

    def remove_actor(self, actor):
        self.actors.remove(actor)

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

    def actor_at(self, loc, source = None):
        for actor in self.actors:
            if actor is source:
                continue
            if loc == actor.loc:
                return actor
        return None

    def random_open(self):
        done = False
        loc = vector(0, 0)
        while not done:
            loc = [random.randint(0, self.dims[0] - 1),
                   random.randint(0, self.dims[1] - 1)]
            loc = vector(loc)
            if not self.is_blocked(loc):
                done = True
        return loc

    class Node(object):
        FLOOR_COST = 10
        STRAIGHT_COST = 9
        OCCUPIED_COST = 40
        
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
        return num_diagonal * World.Node.FLOOR_COST + \
            num_straight * World.Node.STRAIGHT_COST

    def a_star(self, src, dst):
        # set up initial stuff
        grid = self.grid
        dirs = [DIR_NW, DIR_N, DIR_NE, DIR_E,
                DIR_SE, DIR_S, DIR_SW, DIR_W]
        dist = self.heuristic(src, dst)
        q = [World.Node(src, DIR_NONE, 0, dist)]
        totals = [dist]
        finished = set([])
        ret = DIR_NONE

        # main loop
        while len(q) > 0 and ret == DIR_NONE:
            # find the minimum cost node
            cur = q.pop(0)
            totals.pop(0)

            # check if we've reached the goal
            if cur.loc == dst:
                ret = cur.dir
                continue

            # check if already visited
            if cur.loc.tuple() in finished:
                continue
            finished.add(cur.loc.tuple())

            # process neighbors
            for dir in dirs:
                new_loc = grid.move_loc(dir, cur.loc)
                if self.is_blocked(new_loc):
                    continue

                # inherit parent direction if possible
                new_dir = cur.dir
                if new_dir == DIR_NONE:
                    new_dir = dir
                
                # compute the cost of moving to this node
                move_cost = World.Node.FLOOR_COST
                if self.actor_at(new_loc):
                    move_cost = World.Node.OCCUPIED_COST

                # set up the new node
                new_cost = cur.cost + move_cost
                new_heur = self.heuristic(new_loc, dst)
                new_node = World.Node(new_loc, new_dir,
                                      new_cost, new_heur)

                # find location of where to insert new_node
                new_total = new_cost + new_heur
                off = bisect.bisect_right(totals, new_total)
                totals.insert(off, new_total)
                q.insert(off, new_node)
        return ret
