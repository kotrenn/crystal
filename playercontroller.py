from action import *
from squaregrid import *

class PlayerController(object):
    def __init__(self, parent, player, world):
        self.player = player
        self.parent = parent
        self.world = world
        parent.add_key_listener(self)

    def key_pressed(self, key):
        dir = None
        mapping = {
            pygame.K_KP5: DIR_NONE,
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
        grid = self.world.grid

        if key in mapping:
            dir = mapping[key]
            self.player.next_action = WalkAction(self.player, dir)
        
    def key_released(self, key):
        return
