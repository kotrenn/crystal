import pygame
import cProfile
import pstats

from init import *
from mainmenu import *
from player import *
from settings import *

PROFILE = False

def main():
    black = (0, 0, 0)
    size = width, height = 800, 600

    screen = init(size)

    settings = Settings()
    global_font = pygame.font.Font(pygame.font.get_default_font(),
                                   settings.FONT_SIZE)

    player = Player(None)
    window = MainMenu(player)

    if PROFILE:
        pr = cProfile.Profile()
        pr.enable()
        
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                window.key_pressed(event.key)
            elif event.type == pygame.KEYUP:
                window.key_released(event.key)
        
        window.update()
        screen.fill(black)
        window.display(screen)
        pygame.display.flip()

        if window.child is not None:
            window = window.child
        if window.done:
            window = window.parent
            if window is None:
                running = False

    if PROFILE:
        pr.disable()
        sort_by = 'cumulative'
        ps = pstats.Stats(pr).strip_dirs().sort_stats(sort_by)
        ps.print_stats()
        ps.print_callers()

    pygame.quit()

main()
