import pygame

from init import *
from render import *
from settings import *
from vector import *

FONT_SIZE = 20

def get_dir(dims, vec):
    w, h = map(float, dims)
    center = vector(w, h) / 2
    w2, h2 = center.list()
    new_vec = vector(vec.x / w2, vec.y / h2).norm()

    rot_vec = vector(new_vec)
    rot_vec.rotate(-45)

    if rot_vec.x < 0:
        if rot_vec.y < 0:
            return 'NORTH'
        else:
            return 'WEST'
    else:
        if rot_vec.y < 0:
            return 'EAST'
        else:
            return 'SOUTH'

def get_intersection(dims, vec):
    w, h = map(float, dims)
    center = vector(w, h) / 2
    w2, h2 = center.list()
    new_vec = vector(vec.x / w2, vec.y / h2).norm()

    dir = get_dir(dims, vec)
    scale = None
    if dir == 'NORTH':
        scale = -1 / new_vec.y
    elif dir == 'SOUTH':
        scale = 1 / new_vec.y
    elif dir == 'WEST':
        scale = -1 / new_vec.x
    elif dir == 'EAST':
        scale = 1 / new_vec.x

    intersection = scale * new_vec
    #intersection = vector(new_vec)
    intersection %= center
    intersection += center
    return intersection

def main():
    global font
    
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    size = width, height = 800, 600

    screen = init(size)

    settings = Settings()
    global_font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(black)

        pygame.draw.line(screen, blue, (0, 0), (width, height))
        pygame.draw.line(screen, blue, (0, height), (width, 0))
        
        pos = pygame.mouse.get_pos()
        vec = vector(pos) - vector(size) / 2
        dir = get_dir(size, vec)
        intersection = get_intersection(size, vec)

        dims = vector(10, 10)
        rect = intersection - dims / 2
        rect = rect.list() + dims.list()
        center = (width / 2, height / 2)
        pygame.draw.rect(screen, red, rect, 1)
        pygame.draw.line(screen, red, center, intersection.list())

        draw_string(screen, dir, (10, 10), white)
        
        pygame.display.flip()

    pygame.quit()

main()
