# Class for the display of spells.

from hexgridviewer import *
from spell import *

class SpellViewer(Window):
    def __init__(self, parent, spell):
        Window.__init__(self, parent)
        self.spell = spell   # The spell we are currently working with
        self.grid_viewer = HexGridViewer(self.spell.grid) # The grid viewer we are working with

    def display(self, dst):
        # Draw the grid
        self.grid_viewer.display(dst)

        # Draw every crystal
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
                    
        # Draw path overlays to show which crystals are connected
        grid = grid_viewer.grid
        size = grid.size
        start = self.spell.get_source_locs()
        for loc in start:
            edges, cycle = self.spell.get_bfs(loc)
            color = (255, 255, 255)
            # Valid spells do not have cycles.  Notify the player of a cycle.
            if cycle:
                color = (255, 0, 0)
                
            # Draw every edge within the overlay
            for (u, v) in edges:
                c0 = grid_viewer.get_center(u)
                c1 = grid_viewer.get_center(v)
                pygame.draw.line(dst, color, c0.list(), c1.list(), 3)
