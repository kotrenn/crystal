# Base interface for spells.  Includes methods for accessing crystals within the
# spell grid along and for accessing the total combined effects of a spell given
# the player's current layout.

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
        self.type = 'Spell'        # Identifier
        self.player = player       # The player who is using this spell
        self.size = size           # The 'radius' of our spell in number of cells
        self.grid = HexGrid(size)  # Underlying grid we are working with

        # Place in initial 'source' crystals.  These are crystals which players
        # build up their pipe systems from.
        start = self.get_source_locs()
        colors = ((True, False, False),
                  (False, True, False),
                  (False, False, True))
        # For each starting crystal, create and initalize the Crystal object
        for (i, (loc, color)) in enumerate(zip(start, colors)):
            color = Color(*color)
            row, col = loc.list()
            crystal = Crystal()
            
            # Initialize crystal attributes
            crystal.color = color
            crystal.pipes = ['Out'] + [None] * 5
            crystal.atts['Source'] = color
            crystal.atts['Movable'] = False
            
            # Set up the proper orientation
            for _ in range(3 - i):
                crystal.rotate(1)
                
            # Insert the crystal into the grid
            self.grid.cells[row][col] = crystal
            
    # Provide a list of the locations of all source crystals
    def get_source_locs(self):
        grid = self.grid
        size = grid.size
        ret = [(0, 0),
               (size - 1, 0),
               (2 * (size - 1), 0)]
        return map(vector, ret)

    # Perform a breadth-first search on crystals to compute which ones are reachable from
    # the given start crystal.  This is used to determine which crystals are active, and
    # can thus contribute to the overall effects of the spell.
    #
    # Returns a list of edges in the resulting directed graph along with whether
    # a cycle was detected.
    def get_bfs(self, start):
        grid = self.grid
        
        # Make sure there is actually a crystal at start
        if grid.cells[start[0]][start[1]] is None:
            return [], False
            
        dirs = [HEX_NW, HEX_NE, HEX_E, HEX_SE, HEX_SW, HEX_W]
        q = [vector(start)] # Our queue of current nodes
        edges = []
        visited = []
        cycle = False
        # Standard BFS loop
        while len(q) > 0:
            # Get the next location
            cur = q.pop(0)
            row1, col1 = cur.tuple()
            
            # Check if we've already visited
            if cur.list() in visited:
                cycle = True
                continue
            visited.append(cur.list())
            
            # Obtain the actual contents of the cell
            c1 = grid.cells[row1][col1]
            
            # Visit each of the neighboring cells
            neighbors = []
            for dir in dirs:
                loc = grid.move_loc(dir, cur)
                
                # Make sure we're still in bounds
                if grid.out_of_bounds(loc):
                    continue
                
                # Check to see if there is a crystal in the neighboring cell
                row2, col2 = loc.tuple()
                c2 = grid.cells[row2][col2]
                if c2 is None:
                    continue
                
                # Make sure colors match up.  We use <= as opposed to == since
                # some crystal can take more than one color as input.  Yellow
                # can take Red or Green, but output would have to be sent to a
                # crystal which can take both Red and Green.  In this case, these
                # would be Yellow and White crystals.
                if not c1.color <= c2.color:
                    continue
                
                # Make there is an actual pipe going between the two crystals
                if c1.pipes[dir] == 'Out' and \
                   c2.pipes[(dir + 3) % 6] == 'In':
                        edges.append((cur, loc))
                        q.append(loc)
        return edges, cycle

    # Collect a dictionary of all (active) attributes in the spell
    def get_modifiers(self):
        modifiers = ['Neutral', 'Fire', 'Ice', 'Heal', 'Lightning']
        modifiers = {x: 0 for x in modifiers}
        
        # Collect attributes for each source crystal separately
        start = self.get_source_locs()
        for loc in start:
            # Run BFS to find the reachable crystals
            edges, cycle = self.get_bfs(loc)
            
            # Cycles are not allowed for a single source crystals.
            # Merging source crystals is acceptable however.
            if cycle:
                continue
            
            # Don't receive attributes from source crystals or corruption
            # crystals which act as walls.
            forbidden = ['Movable', 'Source']
            cur_modifiers = {}
            
            # Iterate over all edges in the BFS
            for (u, v) in edges:
                # Get the crystal located in cell v
                row, col = v.list()
                crystal = self.grid.cells[row][col]
                
                # Iterate over all attributes the crystal provides
                for (att, val) in crystal.atts.iteritems():
                    # Check if this is a forbidden attribute
                    if att in forbidden:
                        continue
                    
                    # Now increment the value of the attribute
                    # e.g. If att == 'Fire', then increase the Fire damage
                    if att in cur_modifiers:
                        cur_modifiers[att] += val
                    else:
                        cur_modifiers[att] = copy.deepcopy(val)
            
            # We need at least one crystal with the 'Cast' modifier, otherwise
            # no magic is performed from this source crystal.
            if 'Cast' not in cur_modifiers:
                continue
            
            # Add in the contributions from this source crystal to the overall
            # modifiers for the spell
            for (att, val) in cur_modifiers.iteritems():
                if att in modifiers:
                    modifiers[att] += val
                else:
                    modifiers[att] = copy.deepcopy(val)
                    
        # Return sum of all modifiers across the spell
        return modifiers

    # Collect a string description of all attributes provided by the
    # current spell.  Used for display purposes.
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
            
    # Compute the total damage of the spell, broken down by element for
    # any elemental defenses.
    def get_attack(self):
        data = AttackData()
        data.atts = self.get_modifiers()
        return data

    # Displays a simple hexagon icon to represent the spell.  Used in
    # inventory displays that can contain spells.
    def display(self, dst, center, radius):
        color = (255, 255, 255)

        # Compute six different corners for the central hexagon
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
                   
        # Now add in extra points for each outer hexagon.  Uses an
        # ordering to only compute each unique corner point once.
        dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
        points = [[x] for x in range(6)]
        for x in range(6):
            points += [[x, x], [x, x, (x + 1) % 6], 
                       [(x + 1) % 6, (x + 1) % 6, x]]
        zero = vector(0, 0)
        points = [sum([dir_vel[dirs[dir]] for dir in p], zero) for p in points]

        # Build up the list of edges we want to actually draw between points.
        # Separated out so we generate each segment via rotational symmetry.
        segments = [[0, 1, 2, 3, 4, 5, 0]]
        for x in range(6):
            y = 3 * x
            vals = [y, y + 1, y + 2, y + 3]
            vals = [x] + [6 + v % 18 for v in vals]
            segments += [vals]

        # Now actually draw line segments between each point in our hex grid icon.
        for line in segments:
            plist = [center + 0.5 * radius * points[p] for p in line]
            plist = [p.list() for p in plist]
            pygame.draw.lines(dst, color, False, plist)
