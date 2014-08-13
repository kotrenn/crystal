import math
import pygame
import random

from vector import *

class Crystal(object):
    def __init__(self):
        self.color = random.choice([(255, 0, 0),
                                    (0, 255, 0),
                                    (0, 0, 255)])
        self.pipes = [random.choice([True, False]) for _ in range(6)]
        self.pipes = [random.choice(['In', 'Out']) if p else None for p in self.pipes]
        self.atts = {
            'Movable': True
        }

    def display(self, dst, center, radius):
        # draw the crystal core
        num_sides = 8
        points = []
        for i in range(num_sides):
            theta = i * 2.0 * math.pi / num_sides
            t = vector(math.cos(theta), math.sin(theta))
            p = center + radius * t
            points.append(p.list())
        pygame.draw.polygon(dst, self.color, points, 1)

        # draw the pipes
        for (i, pipe) in enumerate(self.pipes):
            if pipe is not None:
                # draw the pipe segment
                offset = i - 2
                theta = offset * 2.0 * math.pi / len(self.pipes)
                t = vector(math.cos(theta), math.sin(theta))
                #radius = 25
                r = 1.7 * radius
                p0 = center
                p1 = center + r * t
                pygame.draw.line(dst, self.color,
                                 p0.list(), p1.list())

                # draw the arrowhead
                r1 = 0.7 * r
                r2 = 0.8 * r
                if pipe == 'Out':
                    r1, r2 = r2, r1
                phi = 5
                p0 = center + r1 * t
                p1 = center + (r2 * t).rotate(-phi)
                p2 = center + (r2 * t).rotate(phi)
                pygame.draw.line(dst, self.color,
                                 p0.list(), p1.list())
                pygame.draw.line(dst, self.color,
                                 p0.list(), p2.list())

    def rotate(self, vel):
        if vel < 0:
            self.pipes = self.pipes[1:] + self.pipes[:1]
        elif vel > 0:
            self.pipes = self.pipes[-1:] + self.pipes[:-1]

    def __str__(self):
        return str(self.color) + ': ' + str(self.pipes)
