from spellviewer import *

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
        corner = vector(30, 400)
        radius = 0.25 * self.grid_viewer.cell_w
        self.crystal_selector.display(dst, corner, radius)

        # draw current crystal info
        crystal = self.crystal_selector.get_selection()
        if crystal is not None:
            corner = vector(400, 400)
            self.crystal_display.display(dst, crystal, corner)

        atts = self.spell.get_atts()
        corner = vector(600, 400)
        color = (255, 255, 255)
        draw_string(dst, atts, corner, color)
