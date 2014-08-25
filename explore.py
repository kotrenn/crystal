from playercontroller import *
from render import *
from settings import *
from window import *
from worldviewer import *
from world import *

class Explore(Window):
    def __init__(self, parent, world, player):
        Window.__init__(self, parent)
        self.world = world
        self.world_viewer = WorldViewer(world)
        self.player = player
        self.player.set_world(world)
        self.player_controller = PlayerController(self, player, world)
        self.world.player = player
        self.current_actor = 0

    def advance_actor(self):
        num_actors = len(self.world.actors)
        self.current_actor = (self.current_actor + 1) % num_actors

    def update(self):
        action = None
        actor = None
        while action is None:
            actor = self.world.actors[self.current_actor]
            if actor.energy.can_take_turn() and actor.needs_input():
                return
            if actor.energy.can_take_turn() or \
               actor.energy.gain(actor.get_speed()):
                if actor.needs_input():
                    return
                action = actor.get_action()
                actor.energy.spend()
            else:
                self.advance_actor()
        action.execute()
        actor.update()
        self.advance_actor()
        
    def display(self, dst):
        self.world_viewer.display(dst)

        # compute offset for the actor list
        settings = Settings()
        dims = vector(self.world.grid.num_cols(), 0)
        text_offset = dims % self.world_viewer.tile_size
        text_offset += vector(20, 0)

        # draw actors and their info
        for (i, actor) in enumerate(self.world.actors):
            # draw the actor
            loc = actor.loc
            pos = self.world_viewer.grid_viewer.get_center(loc)
            actor.display(dst, pos)

            # draw actor info
            text_pos = settings.FONT_SIZE * vector(0, i)
            text_pos += text_offset
            actor_str = actor.name + ' ' + str(actor.hp)
            color = actor.get_color()
            draw_string(dst, actor_str, text_pos, color)

        # draw the player info
        player = self.player
        player_controller = self.player_controller
        dims = vector(0, self.world.grid.num_rows())
        text_offset = dims % self.world_viewer.tile_size
        text_offset += vector(20, 20)
        white = (255, 255, 255)
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        colors = [white, red, green, blue]
        player_str = ''
        player_str += 'HP: ' + str(player.hp) + '\n'
        for mana in player.mana:
            player_str += 'MP: ' + str(mana) + '\n'
        draw_string(dst, player_str, text_offset, colors)

        # draw player spells
        text_offset += vector(150, 0)
        gray = (127, 127, 127)
        spell_list = ''
        for (i, spell) in enumerate(player.spells):
            spell_str = 'Spell ' + str(i + 1)
            spell_str += ' (' + str(spell.size) + ')\n'
            spell_list += spell_str
        colors = [gray for _ in range(len(player.spells))]
        colors[player_controller.spell_selection] = white
        draw_string(dst, spell_list, text_offset, colors)

        # draw current spell info
        text_offset += vector(150, 0)
        spell = player.spells[player_controller.spell_selection]
        att_list = spell.get_atts()
        draw_string(dst, att_list, text_offset, white)
