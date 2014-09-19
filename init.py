import pygame
from settings import *

def init(size):
    passed, failed = pygame.init()
    print 'passed, failed = ' + str((passed, failed))
    pygame.display.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('crystal')
    pygame.font.init()

    print 'Initializing settings...'
    settings = Settings()

    return screen
