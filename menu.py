import pygame
from settings import *
from window import *
from render import *

class Menu(Window):
    def __init__(self, parent, items):
        Window.__init__(self, parent)
        self.items = items
        self.selection = 0

    def key_pressed(self, key):
        Window.key_pressed(self, key)

        if key == pygame.K_UP:
            self.selection -= 1
        elif key == pygame.K_DOWN:
            self.selection += 1
        if self.selection < 0:
            self.selection = len(self.items) - 1
        if self.selection >= len(self.items):
            self.selection = 0

        if key == pygame.K_SPACE or key == pygame.K_z or key == pygame.K_RETURN:
            self.select(self.get_selection())

    def display(self, dst):
        settings = Settings()
        
        image = self.render_image()

        offset_x, offset_y = 0, 0
        if image is not None:
            offset_y = image.get_height()
            dst.blit(image, (0, 0))

        for (i, item) in enumerate(self.items):
            color = (127, 127, 127)
            if i == self.selection:
                color = (255, 255, 255)
            draw_string(dst, item,
                        (offset_x + settings.FONT_SIZE,
                         offset_y + settings.FONT_SIZE * (i + 1)),
                        color)

    def select(self, msg):
        return

    def get_selection(self):
        return self.items[self.selection]

    def remove_selection(self, sel):
        self.items.pop(sel)
        if self.selection > sel:
            self.selection -= 1

    def render_image(self):
        return None
