import copy
import math
import random

from attackdata import *
from crystal import *
from hexgrid import *
from window import *
from vector import *

class Spell(object):
    def __init__(self, player, size):
        self.type = 'Spell'
        self.player = player
        self.size = size
        self.grid = HexGrid(size)

        start = self.get_source_locs()
        colors = ((True, False, False),
                  (False, True, False),
                  (False, False, True))
        for (i, (loc, color)) in enumerate(zip(start, colors)):
            color = Color(*color)
            row, col = loc.list()
            crystal = Crystal()
            crystal.color = color
            crystal.pipes = ['Out'] + [None] * 5
            crystal.atts['Source'] = color
            crystal.atts['Movable'] = False
            for _ in range(3 - i):
                crystal.rotate(1)
            self.grid.cells[row][col] = crystal
            
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
            
        dirs = [HEX_NW, HEX_NE, HEX_E, HEX_SE, HEX_SW, HEX_W]
        q = [vector(start)]
        edges = []
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
                if not c1.color <= c2.color:
                    continue
                if c1.pipes[dir] == 'Out' and \
                   c2.pipes[(dir + 3) % 6] == 'In':
                    edges.append((cur, loc))
                    q.append(loc)
        return edges, cycle

    def get_modifiers(self):
        modifiers = ['Neutral', 'Fire', 'Ice', 'Heal', 'Lightning']
        modifiers = {x: 0 for x in modifiers}
        start = self.get_source_locs()
        for loc in start:
            edges, cycle = self.get_bfs(loc)
            if cycle:
                continue
            forbidden = ['Movable', 'Source']
            cur_modifiers = {}
            for (u, v) in edges:
                row, col = v.list()
                crystal = self.grid.cells[row][col]
                for (att, val) in crystal.atts.iteritems():
                    if att in forbidden:
                        continue
                    if att in cur_modifiers:
                        cur_modifiers[att] += val
                    else:
                        cur_modifiers[att] = copy.deepcopy(val)
            if 'Cast' not in cur_modifiers:
                continue
            for (att, val) in cur_modifiers.iteritems():
                if att in modifiers:
                    modifiers[att] += val
                else:
                    modifiers[att] = copy.deepcopy(val)
        return modifiers

    def get_atts(self):
        ret = ''
        modifiers = self.get_modifiers()
        for (mod, val) in modifiers.iteritems():
            if val == 0:
                continue
            val_str = str(val)
            if isinstance(val, (int, long)):
                val_str = '{:+d}'.format(val)
            ret += str(mod) + ': ' + val_str + '\n'
        return ret
            
    def get_attack(self):
        data = AttackData()
        data.atts = self.get_modifiers()
        return data

    def display(self, dst, center, radius):
        color = (255, 255, 255)

        vels = {
            'N': 90,
            'NE': 30,
            'SE': -30,
            'S': -90,
            'SW': -150,
            'NW': 150
            }
        d2r = math.pi / 180
        dir_vel = {k: vector(math.cos(t * d2r), math.sin(t * d2r))
                   for (k, t) in vels.iteritems()}
        dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
        points = [[x] for x in range(6)]
        for x in range(6):
            points += [[x, x], [x, x, (x + 1) % 6], 
                       [(x + 1) % 6, (x + 1) % 6, x]]
        zero = vector(0, 0)
        points = [sum([dir_vel[dirs[dir]] for dir in p], zero) for p in points]

        segments = [[0, 1, 2, 3, 4, 5, 0]]
        for x in range(6):
            y = 3 * x
            vals = [y, y + 1, y + 2, y + 3]
            vals = [x] + [6 + v % 18 for v in vals]
            segments += [vals]

        for line in segments:
            plist = [center + 0.5 * radius * points[p] for p in line]
            plist = [p.list() for p in plist]
            pygame.draw.lines(dst, color, False, plist)
