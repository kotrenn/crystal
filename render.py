import pygame
from settings import *

def draw_string(dst, msg, p, color):
    settings = Settings()
    font = settings.font

    lines = msg.split('\n')
    for (i, line) in enumerate(lines):
        text = font.render(line, True, color)
        dst.blit(text, (p[0], p[1] + i * settings.FONT_SIZE))
