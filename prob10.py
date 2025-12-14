import scipy as sp
import numpy as np


s = "[##..#...#] (0,1,2,5,6,8) (3,4,5,7,8) (2,3,4) (1,2,4,5,6,7,8) (2,5) (0,5,7) (0,4,5,6,8) {45,33,46,21,45,82,44,43,60}"
s1 = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"


def solve_row_v1(data: str):
    init_state_raw, rest = data.split(" ", 1)
    *buttons_raw, jolts = rest.split(" ")
    init_state = init_state_raw[1:-1]
    buttons = [b[1:-1] for b in buttons_raw]

    def numerize_init(init_str: str):
        bits = ["1" if ch == "#" else "0" for ch in init_str[::-1]]
        res = int("".join(bits), 2)
        return res

    def numerize_button(button_str: str):
        res = 0
        for bit_no in button_str.split(","):
            int_bit_no = int(bit_no)
            res = res | (1 << int_bit_no)
        return res

    def all_subset_idx(bit_size: int):
        masks = [f"{bin(i)[2:]}".rjust(bit_size, "0") for i in range(1 << bit_size)]
        return sorted(masks, key=lambda x: x.count("1"))

    def apply_mask(mask: str, buttons_numerical: list[int]):
        assert len(mask) == len(buttons_numerical)
        res = 0
        for i, c in enumerate(mask):
            if c == "1":
                res = res ^ buttons_numerical[i]
        return res

    subsets = all_subset_idx(len(buttons))
    n = numerize_init(init_state)
    ai = [numerize_button(b) for b in buttons]

    matches = [mask for mask in subsets if apply_mask(mask, ai) == n]
    return min(matches, key=lambda mask: mask.count("1")).count("1")


def solve_v1(path: str):
    with open(path) as f:
        data = f.readlines()
    total = 0
    for line in data:
        total += solve_row_v1(line)
    return total


def solve_row_v2(data: str):
    init_state_raw, rest = data.split(" ", 1)
    *buttons_raw, jolts_raw = rest.split(" ")
    init_state = init_state_raw[1:-1]
    buttons = [b[1:-1] for b in buttons_raw]
    jolts = jolts_raw[1:-1]
    
    b = [int(x) for x in jolts.split(',')]
    A = [[0 for i in range(len(buttons))] for j in range(len(b))]
    
    for i, but in enumerate(buttons):
        idxs = [int(x) for x in but.split(',')]
        for j in idxs:
            A[j][i] = 1

    A = np.array(A)
    b = np.array(b)
    
    m, n = A.shape
    
    c = np.ones(n)
    constraints = sp.optimize.LinearConstraint(A, lb=b, ub=b)
    bounds = sp.optimize.Bounds(lb=np.zeros(n), ub=np.full(n, np.inf))
    integrality = np.ones(n, dtype=int)

    result = sp.optimize.milp(
        c=c,
        constraints=constraints,
        bounds=bounds,
        integrality=integrality
    )

    assert result.success, data
    # if result.success:
    return result.fun
    

def solve_v2(path: str):
    with open(path) as f:
        data = f.readlines()
    total = 0
    for i, line in enumerate(data):
        cur = solve_row_v2(line.strip())
        print(f'{i + 1}: {cur}')
        total += cur
    return total



if __name__ == "__main__":
    res = solve_v2("data/prob-10.txt")
    print(f'{res=}')