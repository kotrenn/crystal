from squaregrid import *

class PlayerController(object):
    def __init__(self, parent, player):
        self.player = player
        self.parent = parent
        parent.add_key_listener(self)

    def key_pressed(self, key):
        dir = None
        mapping = {
            pygame.K_KP7: DIR_NW,
            pygame.K_KP8: DIR_N,
            pygame.K_KP9: DIR_NE,
            pygame.K_KP6: DIR_E,
            pygame.K_KP3: DIR_SE,
            pygame.K_KP2: DIR_S,
            pygame.K_KP1: DIR_SW,
            pygame.K_KP4: DIR_W,
            pygame.K_UP: DIR_N,
            pygame.K_DOWN: DIR_S,
            pygame.K_LEFT: DIR_W,
            pygame.K_RIGHT: DIR_E
        }
        grid = self.parent.grid

        if key in mapping:
            dir = mapping[key]

        new_loc = None
        if dir is not None:
            new_loc = grid.move_loc(dir, self.player.loc)
            if grid.out_of_bounds(new_loc):
                new_loc = None

        if new_loc is not None:
            self.player.loc = new_loc

    def key_released(self, key):
        return