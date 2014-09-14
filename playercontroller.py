from castspellaction import *
from getaction import *
from squaregrid import *
from talkaction import *
from walkaction import *

class PlayerController(object):
    def __init__(self, parent, player, level):
        self.player = player
        self.parent = parent
        self.level = level
        parent.add_key_listener(self)
        self.spell_select = False
        self.spell_selection = 0
        self.talk_select = False

    def key_pressed(self, key):
        if key == pygame.K_s:
            self.spell_select = not self.spell_select
            return

        if key == pygame.K_t:
            self.talk_select = not self.talk_select
            return

        if key == pygame.K_g:
            action = GetAction(self.player, self.player.loc)
            self.player.next_action = action

        mapping = {
            pygame.K_q: -1,
            pygame.K_w: 1
        }
        if key in mapping:
            vel = mapping[key]
            self.spell_selection = (self.spell_selection + vel)
            self.spell_selection %= len(self.player.spells)
            return
        
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
        grid = self.level.grid

        if key in mapping:
            dir = mapping[key]
            action = None
            if self.spell_select:
                if dir == DIR_NONE:
                    return
                self.spell_select = False
                spells = self.player.spells
                spell = spells[self.spell_selection]
                action = CastSpellAction(self.player, spell, dir)
            elif self.talk_select:
                # make this have the player talk to herself (humor)
                if dir == DIR_NONE:
                    return
                self.talk_select = False    
                loc = grid.move_loc(dir, self.player.loc)
                target = self.level.actor_at(loc)
                if target is None:
                    return
                action = TalkAction(self.player, target)
            else:
                action = WalkAction(self.player, dir)
            self.player.next_action = action
        
    def key_released(self, key):
        return
