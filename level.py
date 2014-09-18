import bisect
import heapq
import pygame
import random
import cProfile
import pstats

from monster import *
from npc import *
from squaregrid import *
from vector import *

class Level(object):
    def __init__(self):
        self.dims = vector(12, 17)
        #self.dims = vector(20, 20)
        #self.dims = vector(200, 200)
        #self.dims = vector(12, 50)
        random.seed(4200)
        self.tiles = {
            'blank': [0, 8],
            'tree': [0, 9]
        }
        self.tiles = {k: vector(v) for (k, v) in self.tiles.iteritems()}
        self.grid = SquareGrid(self.dims)
        self.items = SquareGrid(self.dims)
        self.component = SquareGrid(self.dims)
        self.heuristic_cost = {}

        for row in range(self.dims[0]):
            for col in range(self.dims[1]):
                if random.randint(1, 10) <= 3:
                    self.grid.cells[row][col] = self.tiles['tree']
                else:
                    self.grid.cells[row][col] = self.tiles['blank']
                self.items.cells[row][col] = []
                
        # create a row of trees (for testing)
#         for row in range(self.dims[0]):
#             self.grid.cells[row][0] = self.tiles['blank']
#             self.grid.cells[row][1] = self.tiles['tree']
#         self.grid.cells[self.dims[0] - 1][1] = self.tiles['blank']

        self.find_components()

        self.actors = []
        self.actors = [Monster(self) for _ in range(5)]
        self.actors.append(NPC(self))
        self.player = None

        #self.profile()

    def profile(self):
        #initialize stuff
        src = vector(0, 0)
        #dst = vector(self.dims[0] - 1, self.dims[1] - 1)
        dst = self.random_empty()
        
        pr = cProfile.Profile()
        pr.enable()

        # run the actual test
        ret = self.a_star(src, dst)

        # finish profiling
        pr.disable()
        sort_by = 'cumulative'
        ps = pstats.Stats(pr).strip_dirs().sort_stats(sort_by)
        ps.print_stats()
        ps.print_callers()

        print 'ret = ' + str(ret) + ' [' + str(src) + ' ==> ' + str(dst) + ']'

    def find_components(self):
        grid = self.component
        for row in range(grid.num_rows()):
            for col in range(grid.num_cols()):
                grid.cells[row][col] = -1
        cur_component = 0
        for row in range(grid.num_rows()):
            for col in range(grid.num_cols()):
                loc = vector(row, col)
                self.component_dfs(loc, cur_component)
                cur_component += 1

    def component_dfs(self, start_loc, cur_component):
        grid = self.component
        dirs = [DIR_NW, DIR_N, DIR_NE, DIR_E,
                DIR_SE, DIR_S, DIR_SW, DIR_W]

        q = [start_loc]
        while len(q) > 0:
            loc = q.pop()
            row, col = loc.tuple()
            if self.is_blocked(loc):
                continue
            if grid.cells[row][col] >= 0:
                continue
            grid.cells[row][col] = cur_component
            for dir in dirs:
                new_loc = grid.move_loc(dir, loc)
                q.append(new_loc)

    def get_component(self, loc):
        row, col = loc.tuple()
        return self.component.cells[row][col]

    def different_components(self, src, dst):
        comp_src = self.get_component(src)
        comp_dst = self.get_component(dst)
        return comp_src < 0 or comp_dst < 0 or \
            comp_src != comp_dst

    def remove_actor(self, actor):
        if not actor in self.actors:
            return
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

    def random_empty(self):
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
        STRAIGHT_COST = 6
        OCCUPIED_COST = 40
        
        def __init__(self, loc, source_dir, cost, heuristic):
            #self.loc = vector(loc)
            self.loc = loc
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
        # if loc == dst:
        #     return 0
        # if loc in self.heuristic_cost:
        #     return self.heuristic_cost[loc]
        dx = abs(dst.x - loc.x)
        dy = abs(dst.y - loc.y)
        num_diagonal = min(dx, dy)
        num_straight = max(dx, dy) - num_diagonal
        ret = num_diagonal * Level.Node.FLOOR_COST + \
              num_straight * Level.Node.STRAIGHT_COST
        #self.heuristic_cost[loc] = ret
        return ret

    def a_star(self, src, dst):
        # make sure we're in the same component
        if self.different_components(src, dst):
            return DIR_NONE
        
        # set up initial stuff
        self.heuristic_cost = {}
        grid = self.grid
        dirs = [DIR_NW, DIR_N, DIR_NE, DIR_E,
                DIR_SE, DIR_S, DIR_SW, DIR_W]
        ortho = [DIR_N, DIR_E, DIR_S, DIR_W]
        dist = self.heuristic(src, dst)
        start_node = Level.Node(src, DIR_NONE, 0, dist)
        q = [(dist, 0, start_node)]
        count = 1
        dst_actor = self.actor_at(dst)
        finished = set()
        ret = DIR_NONE

        # main loop
        node_count = 0
        while len(q) > 0 and ret == DIR_NONE:
            # find the minimum cost node
            #(_, _, cur) = heapq.heappop(q)
            (x, y, cur) = heapq.heappop(q)
            node_count += 1

            # check if we've reached the goal
            if cur.loc == dst:
                ret = cur.dir
                continue

            # check if already visited
            if cur.loc.tuple() in finished:
                continue
            finished.add(cur.loc.tuple())

            # process neighbors
            base_count = count
            for dir in dirs:
                new_loc = grid.move_loc(dir, cur.loc)
                if new_loc == cur.loc:
                    continue
                if self.is_blocked(new_loc):
                    continue

                # inherit parent direction if possible
                new_dir = cur.dir
                if new_dir == DIR_NONE:
                    new_dir = dir
                
                # compute the cost of moving to this node
                move_cost = Level.Node.FLOOR_COST
                if dir in ortho:
                    move_cost = Level.Node.STRAIGHT_COST
                if self.actor_at(new_loc, dst_actor):
                    move_cost = Level.Node.OCCUPIED_COST

                # set up the new node
                new_cost = cur.cost + move_cost
                new_heur = self.heuristic(new_loc, dst)
                new_node = Level.Node(new_loc, new_dir,
                                      new_cost, new_heur)

                # insert new node into q
                new_total = new_cost + new_heur
                heapq.heappush(q, (new_total, -count, new_node))
                count += 1
        return ret
