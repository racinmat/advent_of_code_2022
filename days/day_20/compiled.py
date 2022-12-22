import numpy as np
from numba import njit
from numba.pycc import CC

cc = CC('my_module')


@cc.export('find', 'i8(types.List(i8), i8)')
@njit('i8(types.List(i8), i8)')
def find(cur_indices, i):
    return [k for k, v in enumerate(cur_indices) if v == i][0]


@cc.export('mix_numbers', 'types.Tuple((i8, types.List(i8), types.List(i8)))(types.List(i8), types.List(i8), types.List(i8), types.List(i8))')
def mix_numbers(numbers, orig_numbers, orig_indices, cur_indices):
    tot_len = len(orig_numbers)
    # print(f'\n{", ".join(map(str, numbers))}')
    for i in orig_indices:
        assert len(set(cur_indices)) == len(cur_indices) == tot_len
        val = orig_numbers[i]
        # I need inverse search, not direct
        cur_idx = find(cur_indices, i)
        new_idx = (cur_idx + val)
        while new_idx >= tot_len:
            new_idx = (new_idx % tot_len) + (new_idx // tot_len)
        while new_idx <= -tot_len:
            new_idx = -(-new_idx % tot_len) - (-new_idx // tot_len)
        del numbers[cur_idx]
        numbers.insert(new_idx, val)
        del cur_indices[cur_idx]
        cur_indices.insert(new_idx, i)
        # print(f'{", ".join(map(str, numbers))}')
    return tot_len, numbers, cur_indices


if __name__ == '__main__':
    # this compiles the numba code, need to call it to compile the extension
    cc.compile()
