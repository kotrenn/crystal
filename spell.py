import random

from crystal import *
from crystalselector import *
from hexgrid import *
from window import *
from vector import *

class Spell(object):
    def __init__(self, player):
        self.player = player
        self.grid = HexGrid(4)

        start = self.get_source_locs()
        colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255))
        for (i, (loc, color)) in enumerate(zip(start, colors)):
            row, col = loc.list()
            crystal = Crystal()
            crystal.color = color
            crystal.pipes = ['Out'] + [None] * 5
            crystal.atts['Source'] = color
            crystal.atts['Movable'] = False
            for _ in range(3 - i):
                crystal.rotate(1)
            self.grid.cells[row][col] = crystal

        for _ in range(10):
            row = random.randint(1, self.grid.num_rows()) - 1
            col = random.randint(1, self.grid.num_cols(row)) - 1
            if self.grid.cells[row][col] is None:
                self.grid.cells[row][col] = Crystal()

    def get_source_locs(self):
        grid = self.grid
        size = grid.size
        ret = [(0, 0),
               (size - 1, 0),
               (2 * (size - 1), 0)]
        return map(vector, ret)

    def get_bfs(self, start):
        grid = self.grid
        if grid.cells[start[0]][start[1]] is None:
            return [], False
            
        dirs = [DIR_NW, DIR_NE, DIR_E, DIR_SE, DIR_SW, DIR_W]
        q = [vector(start)]
        edges = []
        visiting = []
        visited = []
        cycle = False
        while len(q) > 0:
            cur = q.pop(0)
            row1, col1 = cur
            if cur.list() in visited:
                cycle = True
                continue
            visited.append(cur.list())
            c1 = grid.cells[row1][col1]
            neighbors = []
            for dir in dirs:
                loc = grid.move_loc(dir, cur)
                if grid.out_of_bounds(loc):
                    continue
                row2, col2 = loc
                c2 = grid.cells[row2][col2]
                if c2 is None:
                    continue
                if c1.pipes[dir] == 'Out' and \
                   c2.pipes[(dir + 3) % 6] == 'In':
                    edges.append((cur, loc))
                    q.append(loc)
        return edges, cycle

    def get_atts(self):
        modifiers = ['Fire', 'Ice', 'Heal', 'Lightning']
        modifiers = {x: 0 for x in modifiers}
        start = self.get_source_locs()
        for loc in start:
            edges, cycle = self.get_bfs(loc)
            if cycle:
                continue
            forbidden = ['Movable', 'Source']
            for (u, v) in edges:
                row, col = v.list()
                crystal = self.grid.cells[row][col]
                for (att, val) in crystal.atts.iteritems():
                    if att in forbidden:
                        continue
                    if att in modifiers:
                        modifiers[att] += int(val)
                    #ret += str(att) + ': ' + str(val) + '\n'
        ret = ''
        for (mod, val) in modifiers.iteritems():
            if val == 0:
                continue
            ret += str(mod) + ': {:+d}\n'.format(val)
        return ret
            
