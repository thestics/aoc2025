from dataclasses import dataclass


def read_input(path: str):
    with open(path) as f:
        data = f.read()
    
    ranges = []
    ids = []
    mode = 'ranges'
    for row in data.split('\n'):
        if not row:
            mode = 'ids'
            continue
            
        if mode == 'ranges':
            l, r = row.split('-')
            ranges.append((int(l), int(r)))
        elif mode == 'ids':
            ids.append(int(row))
    return ranges, ids


def solve_v1():
    ranges, ids = read_input('data/prob5.txt')
    # print(ranges)
    # print(ids)

    total = 0
    for i, val in enumerate(ids):
        print(f'{i + 1}/{len(ids)}: {val}')
        fresh = False
        for left, right in ranges:
            if left <= val <= right:
                fresh = True
                break
        if fresh:
            total += 1
    print(f'{total=}')


@dataclass
class Range:
    left: int
    right: int


def solve_v2():
    ranges, _ = read_input('data/prob5.txt')
    ranges = [Range(left=rng[0], right=rng[1]) for rng in ranges]
    sorted_ranges = sorted(ranges, key=lambda x: x.left)
    disjoint_ranges = []

    cur = sorted_ranges[0]

    for rng in sorted_ranges[1:]:
        if rng.left <= cur.right:
            cur.right = max(cur.right, rng.right)
            # cur.right = rng.right
        else:
            disjoint_ranges.append(cur)
            cur = rng
    disjoint_ranges.append(cur)
    total_size = sum(r.right - r.left + 1 for r in disjoint_ranges)
    print(f"{disjoint_ranges=} {total_size=}")


solve_v2()