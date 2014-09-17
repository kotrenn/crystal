from squaregrid import *

class SquareGridViewer(object):
    def __init__(self, grid, size):
        self.grid = grid
        self.cell_w = size[0]
        self.cell_h = size[1]

    def get_center(self, loc):
        row = loc[0]
        col = loc[1]
        offset = vector(col * self.cell_w,
                        row * self.cell_h)
        offset += 0.5 * vector(self.cell_w, self.cell_h)
        return offset

    def display(self, dst):
        return
        dims = vector(self.cell_w, self.cell_h)
        white = (255, 255, 255)
        for row in range(self.grid.num_rows()):
            for col in range(self.grid.num_cols()):
                self.draw_square(dst, [row, col], dims, white)

    def draw_square(self, dst, loc, dims, color):
        row = loc[0]
        col = loc[1]
        points = [(-0.5, -0.5), (0.5, -0.5),
                  (0.5, 0.5), (-0.5, 0.5)]
        center = self.get_center(loc)
        final = []
        for p in points:
            pos = vector(p)
            point = center + pos % dims
            final.append(point.list())
        pygame.draw.polygon(dst, color, final, 1)
