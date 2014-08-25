from crystaldisplay import *
from hexgridviewer import *
from spell import *

class SpellViewer(Window):
    def __init__(self, parent, spell):
        Window.__init__(self, parent)
        self.spell = spell
        self.grid_viewer = HexGridViewer(self.spell.grid)
        self.crystal_display = CrystalDisplay()

    def display(self, dst):
        # draw the grid
        self.grid_viewer.display(dst)

        # draw every crystal
        grid_viewer = self.grid_viewer
        grid = grid_viewer.grid
        for row in range(grid.num_rows()):
            for col in range(grid.num_cols(row)):
                crystal = grid.cells[row][col]
                if crystal is None:
                    continue
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
                pygame.draw.line(dst, color, c0.list(), c1.list(), 3)
