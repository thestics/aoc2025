from collections import deque
from dataclasses import dataclass
from rich import print as rprint

@dataclass
class Point:
    x: int
    y: int
    z: int


def d2(p1: Point, p2: Point):
    "Squared distance"
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2


def read_input(p: str):
    with open(p) as f:
        lines = f.readlines()
    pts = [Point(*[int(x) for x in line.split(',')]) for line in lines]
    return pts


def build_dist_list(pts: list[Point]):
    res = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            res.append((
                (i, j),
                d2(pts[i], pts[j])
            ))
    return sorted(res, key=lambda x: x[1])


TPointID = int
TPointPairIDS = tuple[TPointID, TPointID]
TDist = int
def build_clusters(pts: list[Point], dist_list: list[tuple[TPointPairIDS, TDist]], rounds: int | None = 1000):
    clst_map = {}
    map_size = {}
    idx = 0
    deq = deque(dist_list)
    total_rounds = rounds if rounds is not None else len(dist_list)

    for round_no in range(total_rounds):
        ((l_idx, r_idx), dist) = deq.popleft()
        print(f'{l_idx=} {r_idx=} {dist=}:', end=' ')

        # op1: both are not in a cluster
        if l_idx not in clst_map and r_idx not in clst_map:
            print('BOTH_NEW')
            clst_map[l_idx] = idx
            clst_map[r_idx] = idx
            map_size[idx] = 2
            idx += 1
        # op2: one of two in a cluster
        elif l_idx in clst_map and r_idx not in clst_map:
            print('RIGHT_NEW')
            clst_map[r_idx] = clst_map[l_idx]
            map_size[clst_map[l_idx]] += 1
        elif l_idx not in clst_map and r_idx in clst_map:
            print('LEFT_NEW')
            clst_map[l_idx] = clst_map[r_idx]
            map_size[clst_map[r_idx]] += 1
        # op3.1: both are in the cluster (same)
        # no need to do anything

        # op3.2: both are in the cluster (different)
        elif l_idx in clst_map and r_idx in clst_map and clst_map[l_idx] != clst_map[r_idx]:
            print('MERGE')
            old_clst_idx = clst_map[r_idx]
            new_clst_idx = clst_map[l_idx]

            map_size[new_clst_idx] = map_size[old_clst_idx] + map_size[new_clst_idx]
            map_size.pop(old_clst_idx)
            if len(map_size) == 1:
                # rprint('Final:', pts[l_idx], pts[r_idx])
                return clst_map, (pts[l_idx], pts[r_idx])

            for k, v in clst_map.items():
                if v == old_clst_idx:
                    clst_map[k] = new_clst_idx
        else:
            print('SKIP')
        # print(f"{round_no=}", map_size)
    return clst_map, None


def solve1():
    pts = read_input('data/prob-8.txt')
    dists = build_dist_list(pts)
    clusters, _ = build_clusters(pts, dists, rounds=1000)
    grouped = {}
    for k, v in clusters.items():
        grouped[v] = grouped.get(v, 0) + 1

    target = list(grouped.values())
    max1 = max(target)
    target.remove(max1)
    max2 = max(target)
    target.remove(max2)
    max3 = max(target)
    print(f'Top 3 cluster sizes: {max1, max2, max3}')
    return max1 * max2 * max3


def solve2():
    pts = read_input('data/prob-8.txt')
    dists = build_dist_list(pts)
    clusters, crucial_points = build_clusters(pts, dists, rounds=None)
    rprint(crucial_points)
    print(crucial_points[0].x * crucial_points[1].x)


if __name__ == '__main__':
    print(solve1())
    # solve2()
    # pts = read_input('data/prob-8.txt')
    # # rprint(pts)
    # dists = build_dist_list(pts)
    # # print(dists)
    # # rprint(dists)
    # clusters, crucial_points = build_clusters(pts, dists, rounds=None)
    # rprint(crucial_points)
    # print(crucial_points[0].x * crucial_points[1].x)
    
    # rprint(clusters)
    # grouped = {}
    # for k, v in clusters.items():
    #     grouped[v] = grouped.get(v, 0) + 1
    # rprint(grouped)
    # target = list(grouped.values())
    # rprint(target)
    # max1 = max(target)
    # target.remove(max1)
    # max2 = max(target)
    # target.remove(max2)
    # max3 = max(target)

    # print(f'Product: {max1 * max2 * max3}')
    # rprint(sorted(list(clusters.items()), key=lambda x: x[1]))
