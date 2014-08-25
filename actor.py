from energy import *
from gamestat import *
from settings import *
from squaregrid import *

class Actor(object):
    def __init__(self, world):
        self.loc = vector(0, 0)
        self.world = world
        self.speed = Energy.NORMAL_SPEED
        self.energy = Energy()
        self.set_world(world)
        self.die_at_wall = False
        self.name = 'Actor'
        self.hp = GameStat(0)

    def set_world(self, world):
        self.world = world
        if world is None:
            return
        if self not in self.world.actors:
            self.world.actors.append(self)

    def has_class(self, class_name):
        classes = str(type.mro(type(self)))
        modified_name = "." + class_name + "'"
        return modified_name in classes

    def needs_input(self):
        return False

    def get_action(self):
        return None

    def default_attack(self, target):
        return None

    def get_symbol(self):
        return '@'

    def get_color(self):
        return (255, 255, 255)

    def get_speed(self):
        return self.speed

    def display(self, dst, center):
        settings = Settings()
        font = settings.font
        color = self.get_color()
        text = font.render(self.get_symbol(), True, color)
        loc = center - 0.5 * vector(text.get_size())
        dst.blit(text, loc.list())
