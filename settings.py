import pygame

class Settings(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls, *args, **kwargs)
            Settings.init(cls._instance)
        return cls._instance

    def init(self):
        self.FONT_SIZE = 20
        self.font = pygame.font.Font(pygame.font.get_default_font(),
                                     self.FONT_SIZE)
