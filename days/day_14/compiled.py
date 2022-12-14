from numba.pycc import CC
import numpy as np

# it's both the same, we don't need to distinguish between them
FILLED = 1

cc = CC('my_module')


@cc.export('simulate_sand', 'i8(i1[:, :])')
def simulate_sand(grid):
    infinite_fall = False
    y_start = 500
    i = -1
    while not infinite_fall:
        i += 1
        new_x, new_y = 0, y_start
        falling = True
        while falling:
            grounds = np.where(grid[new_x:, new_y])[0]
            if len(grounds) > 0:
                x_ground = grounds[0]
            else:
                infinite_fall = True
                break
            new_x, new_y = new_x + x_ground - 1, new_y
            # look left down
            if not grid[new_x + 1, new_y - 1]:
                new_x, new_y = new_x + 1, new_y - 1
            elif not grid[new_x + 1, new_y + 1]:
                new_x, new_y = new_x + 1, new_y + 1
            else:
                falling = False
        grid[new_x, new_y] = FILLED
        if (new_x, new_y) == (0, y_start):
            break
    return i


if __name__ == '__main__':
    # this compiles the numba code, need to call it to compile the extension
    cc.compile()
