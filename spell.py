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
            else:
                visited.append(cur.list())
                c1 = grid.cells[row1][col1]
                neighbors = []
                for dir in dirs:
                    loc = grid.move_loc(dir, cur)
                    if not grid.out_of_bounds(loc):
                        row2, col2 = loc
                        c2 = grid.cells[row2][col2]
                        if c2 is not None:
                            if c1.pipes[dir] == 'Out' and \
                               c2.pipes[(dir + 3) % 6] == 'In':
                                edges.append((cur, loc))
                                q.append(loc)
        return edges, cycle

class SpellViewer(Window):
    def __init__(self, parent, spell):
        Window.__init__(self, parent)
        self.spell = spell
        self.grid_viewer = HexGridViewer(self.spell.grid)

    def display(self, dst):
        self.grid_viewer.display(dst)

        # draw every crystal
        grid_viewer = self.grid_viewer
        grid = grid_viewer.grid
        for row in range(grid.num_rows()):
            for col in range(grid.num_cols(row)):
                crystal = grid.cells[row][col]
                if crystal is not None:
                    center = grid_viewer.get_center((row, col))
                    radius = 0.25 * grid_viewer.cell_w
                    crystal.display(dst, center, radius)
                    
        # draw path stuff
        grid = grid_viewer.grid
        size = grid.size
        start = self.spell.get_source_locs()
        for loc in start:
            edges, cycle = self.spell.get_bfs(loc)
            color = (255, 255, 255)
            if cycle:
                color = (255, 0, 0)
            for (u, v) in edges:
                c0 = grid_viewer.get_center(u)
                c1 = grid_viewer.get_center(v)
                pygame.draw.line(dst, color, c0.list(), c1.list())

class SpellEditor(SpellViewer):
    def __init__(self, parent, spell):
        SpellViewer.__init__(self, parent, spell)
        self.spell = spell
        size = self.spell.grid.size
        self.select = vector(size - 1, size - 1)
        self.prev_select = vector(0, 0)
        self.moving = False
        self.crystal_selector = CrystalSelector(self, spell.player.crystals)

    def key_released(self, key):
        SpellViewer.key_released(self, key)
        
        # movement along the grid
        dir = None
        mapping = {
            pygame.K_w: DIR_NW,
            pygame.K_s: DIR_SE,
            pygame.K_a: DIR_W,
            pygame.K_d: DIR_E,
            pygame.K_u: DIR_NW,
            pygame.K_i: DIR_NE,
            pygame.K_k: DIR_E,
            pygame.K_m: DIR_SE,
            pygame.K_n: DIR_SW,
            pygame.K_h: DIR_W
            }
        if key in mapping:
            dir = mapping[key]
            
        new_loc = None
        if dir is not None:
            grid = self.spell.grid
            new_loc = grid.move_loc(dir, self.select)
            if grid.out_of_bounds(new_loc):
                new_loc = None
        
        if new_loc is not None:
            self.select = new_loc

        # swap two crystal cells
        if key == pygame.K_x or key == pygame.K_SPACE:
            row1, col1 = self.select.list()
            grid = self.spell.grid
            movable = True
            if grid.cells[row1][col1] is not None:
                if not grid.cells[row1][col1].atts['Movable']:
                    movable = False
            if movable:
                if self.moving:
                    row2, col2 = self.prev_select.list()
                    tmp = grid.cells[row1][col1]
                    grid.cells[row1][col1] = grid.cells[row2][col2]
                    grid.cells[row2][col2] = tmp
                    self.moving = False
                else:
                    self.prev_select = vector(self.select)
                    self.moving = True

        # rotate the current crystal
        if key == pygame.K_q:
            row, col = self.select.list()
            grid = self.spell.grid
            if grid.cells[row][col] is not None:
                grid.cells[row][col].rotate(-1)
        elif key == pygame.K_e:
            row, col = self.select.list()
            grid = self.spell.grid
            if grid.cells[row][col] is not None:
                grid.cells[row][col].rotate(1)

        # exchange with the crystal selection grid
        if key == pygame.K_c:
            row, col = self.select.list()
            grid = self.spell.grid
            if grid.cells[row][col] is None:
                selector = self.crystal_selector
                crystal = selector.get_selection()
                selector.remove_selection()
                grid.cells[row][col] = crystal
        if key == pygame.K_v:
            row, col = self.select
            grid = self.spell.grid
            if grid.cells[row][col] is not None:
                crystal = grid.cells[row][col]
                if crystal.atts['Movable']:
                    grid.cells[row][col] = None
                    self.crystal_selector.add_crystal(crystal)

    def display(self, dst):
        SpellViewer.display(self, dst)

        # draw the grid
        grid_viewer = self.grid_viewer

        # highlight the currently selected cell
        dims = 0.9 * vector(grid_viewer.cell_w,
                            grid_viewer.cell_h)
        white = (255, 255, 255)
        self.grid_viewer.draw_hex(dst, self.select, dims, white)

        # draw the previous selection (if applicable)
        if self.moving:
            red = (255, 0, 0)
            self.grid_viewer.draw_hex(dst, self.prev_select, dims, red)

        # draw crystal selections
        corner = vector(30, 500)
        radius = 0.25 * self.grid_viewer.cell_w
        self.crystal_selector.display(dst, corner, radius)
