# Interface for allowing players to configure their personal spells.
# Extends SpellViewer which handles display of the spell itself.

from crystalsummary import *
from itemselector import *
from spellviewer import *

class SpellEditor(SpellViewer):
    def __init__(self, parent, spell):
        SpellViewer.__init__(self, parent, spell)
        self.spell = spell                       # The spell we are working with
        size = self.spell.grid.size              # Size (in pixels) of each cell
        self.select = vector(size - 1, size - 1) # Current location of the player cursor in the grid
        self.prev_select = vector(0, 0)          # Used for swapping two crystals
        self.moving = False                      # Flag for if we are currently swapping two crystals
        self.crystal_selector = ItemSelector(self, spell.player.crystals) # Display interface for selecting crystals
        self.crystal_summary = CrystalSummary()  # Tool for displaying information about the currently selected crystal

    # Handle input
    def key_released(self, key):
        SpellViewer.key_released(self, key)
        
        # Movement along the grid
        dir = None
        mapping = {
            pygame.K_w: HEX_NW,
            pygame.K_s: HEX_SE,
            pygame.K_a: HEX_W,
            pygame.K_d: HEX_E,
            pygame.K_u: HEX_NW,
            pygame.K_i: HEX_NE,
            pygame.K_k: HEX_E,
            pygame.K_m: HEX_SE,
            pygame.K_n: HEX_SW,
            pygame.K_h: HEX_W
        }
        
        # Check if one of the movement keys has been pressed
        if key in mapping:
            dir = mapping[key]
            
        # Now compute the next location
        new_loc = None
        if dir is not None:
            grid = self.spell.grid
            new_loc = grid.move_loc(dir, self.select)
            if grid.out_of_bounds(new_loc):
                new_loc = None
                # TODO: implement "sliding" for when players
                #       push off the edge of the grid
        
        # Move to the next location if within bounds
        if new_loc is not None:
            self.select = new_loc

        # Swap two crystal cells
        if key == pygame.K_x or key == pygame.K_SPACE:
            row1, col1 = self.select.list()
            grid = self.spell.grid
            
            # Check to make sure we can actually move this crystal
            movable = True
            if grid.cells[row1][col1] is not None:
                if not grid.cells[row1][col1].atts['Movable']:
                    movable = False
            
            # If we have permission, move it
            if movable:
                # Check if we already have a crystal selected
                if self.moving:
                    # Swap two crystals and reset movement flag
                    row2, col2 = self.prev_select.list()
                    tmp = grid.cells[row1][col1]
                    grid.cells[row1][col1] = grid.cells[row2][col2]
                    grid.cells[row2][col2] = tmp
                    self.moving = False
                else:
                    # Take a note of where we selected
                    self.prev_select = vector(self.select)
                    self.moving = True

        # Rotate the current crystal counter-clockwise
        if key == pygame.K_q:
            row, col = self.select.list()
            grid = self.spell.grid
            if grid.cells[row][col] is not None:
                grid.cells[row][col].rotate(-1)
                
        # Rotate the current crystal clockwise
        elif key == pygame.K_e:
            row, col = self.select.list()
            grid = self.spell.grid
            if grid.cells[row][col] is not None:
                grid.cells[row][col].rotate(1)

        # Bring the currently selected crystal in the selector into the current cell
        if key == pygame.K_c:
            row, col = self.select.list()
            grid = self.spell.grid
            if grid.cells[row][col] is None:
                selector = self.crystal_selector
                crystal = selector.get_selection()
                selector.remove_selection()
                grid.cells[row][col] = crystal
        
        # Remove the currently selected crystal and place it into the player's crystal inventory
        if key == pygame.K_v:
            row, col = self.select.list()
            grid = self.spell.grid
            if grid.cells[row][col] is not None:
                crystal = grid.cells[row][col]
                if crystal.atts['Movable']:
                    grid.cells[row][col] = None
                    self.crystal_selector.add_item(crystal)

    # Draw everything
    def display(self, dst):
        SpellViewer.display(self, dst)

        # Get the current grid viewer
        grid_viewer = self.grid_viewer

        # Highlight the currently selected cell
        dims = 0.9 * vector(grid_viewer.cell_w,
                            grid_viewer.cell_h)
        white = (255, 255, 255)
        self.grid_viewer.draw_hex(dst, self.select, dims, white)

        # Draw the previous selection (if applicable)
        if self.moving:
            red = (255, 0, 0)
            self.grid_viewer.draw_hex(dst, self.prev_select, dims, red)

        # Draw the crystal inventory/selector
        corner = vector(30, 400)
        radius = 0.25 * self.grid_viewer.cell_w
        self.crystal_selector.display(dst, corner, radius)

        # Display information on the current crystal
        crystal = self.crystal_selector.get_selection()
        if crystal is not None:
            corner = vector(400, 400)
            self.crystal_summary.display(dst, crystal, corner)

        # Display the current effects produced by the spell
        atts = self.spell.get_atts()
        corner = vector(600, 400)
        color = (255, 255, 255)
        draw_string(dst, atts, corner, color)
