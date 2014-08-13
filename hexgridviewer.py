from hexgrid import *

class HexGridViewer(object):
    def __init__(self, grid):
        self.grid = grid
        self.cell_w = 50
        self.cell_h = 50
        #self.cell_w = self.cell_h = 100

    def get_center(self, loc):
        row = loc[0]
        col = loc[1]
        empty = abs(self.grid.size - 1 - row)
        empty_x = empty / 2.0
        offset = vector((col + empty_x) * self.cell_w,
                        0.75 * row * self.cell_h)
        offset += 0.5 * vector(self.cell_w, self.cell_h)
        return offset
        
    def display(self, dst):
        dims = vector(self.cell_w, self.cell_h)
        size = self.grid.size
        max_row = 2 * size - 1
        for row in range(max_row):
            empty = abs(size - 1 - row)
            num_cols = max_row - empty
            for col in range(num_cols):
                white = (255, 255, 255)
                self.draw_hex(dst, [row, col], dims, white)

    def draw_hex(self, dst, loc, dims, color):
        row = loc[0]
        col = loc[1]
        points = [(0, -0.5), (0.5, -0.25),
                  (0.5, 0.25), (0, 0.5),
                  (-0.5, 0.25), (-0.5, -0.25)]
        center = self.get_center(loc)
        final = []
        for p in points:
            pos = vector(p)
            point = center + pos % dims
            final.append(point.list())
        pygame.draw.polygon(dst, color, final, 1)
