import pygame
from settings import *

def draw_string(dst, msg, p, colors):
    # print 'draw_string(['
    # for line in msg.split('\n'):
    #     print '             ' + line + ','
    # print '            ]'
    # print '            ' + str(p)
    # print '            ' + str(colors)
    # print '            )'
    settings = Settings()
    font = settings.font

    lines = msg.split('\n')
    for (i, line) in enumerate(lines):
        color = None
        if isinstance(colors, list):
            color = colors[i % len(colors)]
        else:
            color = colors
        text = font.render(line, True, color)
        dst.blit(text, (p[0], p[1] + i * settings.FONT_SIZE))
