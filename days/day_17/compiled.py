import numpy as np
from numba.pycc import CC

cc = CC('my_module')


@cc.export('simulate_tetris', 'types.Tuple((i1[:, :], i4[:], i1[:]))(types.unicode_type, types.List(b1[:, ::1], reflected=True), i8, i8)')
def simulate_tetris(pattern, shapes, depth, n_steps):
    grid = np.zeros((depth, 7), dtype=np.int8)
    blocks = - np.ones(depth, dtype=np.int32)
    heights = np.zeros(n_steps, dtype=np.int8)
    tot_width = grid.shape[1]
    j = -1
    old_height = depth
    max_height = depth
    for i in range(n_steps):
        shape = shapes[i % len(shapes)]
        height, width = shape.shape
        x = 2
        if np.all(grid == 0):
            y = depth - 3
        else:
            max_line = np.count_nonzero(grid, 1) > 0
            y = np.argmax(max_line, 0) - 3
        # print(f'{i}th starts falling: {x=},{y=}')
        even = False
        hit_floor = False
        while True:
            old_x, old_y = x, y
            if even:
                y += 1
                # print(f'falls down to {x=},{y=}')
                if y > depth:
                    hit_floor = True
                    break
            else:
                j += 1
                j %= len(pattern)
                p = pattern[j]
                if p == '>':
                    x = min(x + 1, tot_width - width)
                    added_shape = grid[y - height:y, x:x + width] + shape
                    if np.any(added_shape > 1):
                        # not moving
                        x = old_x
                    # print(f'pushes right{", nothing happens" if x == tot_width - width else ""}, {x=}, {y=}')
                else:
                    x = max(x - 1, 0)
                    added_shape = grid[y - height:y, x:x + width] + shape
                    if np.any(added_shape > 1):
                        # not moving
                        x = old_x
                    # print(f'pushes left{", nothing happens" if x == 0 else ""}, {x=}, {y=}')
            even = not even
            if hit_floor:
                break
            else:
                added_shape = grid[y - height:y, x:x + width] + shape
                if np.any(added_shape > 1):
                    break
        grid[old_y - height:old_y, old_x:old_x + width] += shape
        blocks[old_y - height:old_height] = i
        heights[i] = max(max_height - (old_y - height), 0)
        old_height = old_y - height
        max_height = min(max_height, old_y - height)
    return grid, blocks, heights


if __name__ == '__main__':
    # this compiles the numba code, need to call it to compile the extension
    cc.compile()
