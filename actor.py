from color import *
from energy import *
from gamestat import *
from settings import *
from squaregrid import *

class Actor(object):
    def __init__(self, level):
        self.loc = vector(0, 0)
        self.prev_vel = vector(0, 0)
        self.level = level
        self.speed = Energy.NORMAL_SPEED
        self.energy = Energy()
        self.set_level(level)
        self.die_at_wall = False
        self.name = 'Actor'
        self.hp = GameStat(0)

    def set_level(self, level):
        self.level = level
        if level is None:
            return
        if self not in self.level.actors:
            self.level.actors.append(self)

    def has_class(self, class_name):
        classes = str(type.mro(type(self)))
        modified_name = "." + class_name + "'"
        return modified_name in classes

    def update(self):
        return

    def heal(self, hp):
        self.hp.add(hp)

    def get_mana(self):
        return Color()

    def burn_mana(self, mana_cost):
        return

    def needs_input(self):
        return False

    def get_action(self):
        return None

    def default_attack(self, target, dir):
        return None

    def talk_to(self, source):
        return

    def get_symbol(self):
        return '@'

    def get_color(self):
        return (255, 255, 255)

    def get_speed(self):
        return self.speed

    def walk_to(self, loc, vel):
        self.loc = loc
        self.prev_vel = vel

    def display(self, dst, center):
        settings = Settings()
        font = settings.font
        color = self.get_color()
        text = font.render(self.get_symbol(), True, color)
        loc = center - 0.5 * vector(text.get_size())
        dst.blit(text, loc.list())
