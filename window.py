import pygame

class Window(object):
    def __init__(self, parent):
        self.parent = parent
        self.child = None
        self.done = False
        self.key_listeners = []

    def add_key_listener(self, listener):
        self.key_listeners.append(listener)

    def key_pressed(self, key):
        for listener in self.key_listeners:
            listener.key_pressed(key)

    def key_released(self, key):
        if key == pygame.K_ESCAPE:
            self.exit()
        for listener in self.key_listeners:
            listener.key_released(key)

    def update(self):
        return

    def display(self, dst):
        return

    def exit(self):
        self.done = True
        if self.parent is not None:
            self.parent.child = None
