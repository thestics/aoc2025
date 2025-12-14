from collections import deque
from copy import deepcopy
from dataclasses import dataclass
import numpy as np


@dataclass
class Point:
    x: int
    y: int

    def vec_to(self, end: "Point"):
        return self.__class__(end.x - self.x, end.y - self.y)

    def area(self, other: "Point"):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return (dx + 1) * (dy + 1)

def cross_prod(v1: Point, v2: Point):
    return v1.x*v2.y - v1.y*v2.x
    # return np.cross([v1.x, v1.y, 0], [v2.x, v2.y, 0])[2]


@dataclass
class Triangle:
    p1: Point
    p2: Point
    p3: Point

    def contains(self, p: Point):
        pts = [self.p1, self.p2, self.p3]
        prods = []
        for cur, next in zip(pts, pts[1:] + pts[:1]):
            v1 = cur.vec_to(next)
            v2 = cur.vec_to(p)
            prod = cross_prod(v1, v2)
            if abs(prod) < 1e-9:
                continue
            prods.append(prod)
        prod_signs = [p > 0 for p in prods]
        return all(prod_signs) or all([not x for x in prod_signs])


@dataclass
class Segment:
    p1: Point
    p2: Point

    def intersects_exclusive(self, other: "Segment"):
        min_px = min(self.p1.x, self.p2.x)
        max_px = max(self.p1.x, self.p2.x)
        min_py = min(self.p1.y, self.p2.y)
        max_py = max(self.p1.y, self.p2.y)
        
        min_tx = min(other.p1.x, other.p2.x)
        max_tx = max(other.p1.x, other.p2.x)
        min_ty = min(other.p1.y, other.p2.y)
        max_ty = max(other.p1.y, other.p2.y)
        
        cond1 = min_py < min_ty < max_py and \
                min_tx < min_px < max_tx
        cond2 = min_ty < min_py < max_ty and \
                min_px < min_tx < max_px
        return cond1 or cond2 


def rec_contains_seg(p1: Point, p2: Point, s: Segment):
    t1 = s.p1
    t2 = s.p2

    min_px = min(p1.x, p2.x)
    max_px = max(p1.x, p2.x)
    min_py = min(p1.y, p2.y)
    max_py = max(p1.y, p2.y)
    
    min_tx = min(t1.x, t2.x)
    max_tx = max(t1.x, t2.x)
    min_ty = min(t1.y, t2.y)
    max_ty = max(t1.y, t2.y)
    
    cond1 = min_py < min_ty < max_py and \
            min_tx == min(min_px, max_px) and max_tx == max(min_px, max_px)
    cond2 = min_px < min_tx < max_px and \
            min_ty == min(min_py, max_py) and max_ty == max(min_py, max_py)
    return cond1 or cond2


def read_input(path: str):
    with open(path) as f:
        points = [Point(*[int(x) for x in line.split(',')]) for line in f.readlines()]
        return points


def solve_1(path: str):
    points = read_input(path)    
    best = -1
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = points[i]
            p2 = points[j]
            area = abs(p1.x - p2.x + 1) * abs(p1.y - p2.y + 1)
            print(f"{p1=} {p2=} {area=} {best=} ", end='')
            if area > best:
                best = area
                print('NEW_BEST')
            else:
                print()
            
    print(f'{best=}')


def triangulate_ears(data: list[Point]):
    triangles = []
    pts = deque(deepcopy(data))
    
    def accept_triangle(p1, p2, p3):
        # save triangle, remove middle point, rotate
        # so that we move in concentric circles
        triangles.append(Triangle(p1, p2, p3))
        pts.appendleft(p3)
        pts.append(p1)
    
    def reject_triangle(p1, p2, p3):
        # rotate points, so that we move in 
        # concentric circles
        pts.appendleft(p3)
        pts.appendleft(p2)
        pts.append(p1)

    while len(pts) >= 3:
        print(f'Triangulation: {len(pts)} points left')
        p1 = pts.popleft()
        p2 = pts.popleft()
        p3 = pts.popleft()

        v1 = p1.vec_to(p2)
        v2 = p2.vec_to(p3)
        cross = cross_prod(v1, v2)

        # angle should be internal
        if cross > 0:
            candidate = Triangle(p1, p2, p3)
            contains_others = False
            
            # check if candidate triangle contains any other polygon points
            for other_p in pts:
                if candidate.contains(other_p):
                    contains_others = True
                    break
            
            if not contains_others:
                accept_triangle(p1, p2, p3)
            else:
                reject_triangle(p1, p2, p3)
        else:
            reject_triangle(p1, p2, p3)
    
    return triangles


from rich import print as rprint
def solve_2(path: str):
    points = read_input(path)
    print('Triangulation...')
    triangulation = triangulate_ears(points)
    rprint(triangulation)
    acceptable_corners = []
    print('Validating corners')
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            print(f'Corners {len(points) * i + j}/{len(points)**2}...')
            # 1   3
            # | / |
            # 2   4
            p1 = points[i]
            p2 = points[j]

            corners_to_test = [
                Point(min(p1.x, p2.x), min(p1.y, p2.y)),
                Point(min(p1.x, p2.x), max(p1.y, p2.y)),
                Point(max(p1.x, p2.x), min(p1.y, p2.y)),
                Point(max(p1.x, p2.x), max(p1.y, p2.y)),
            ]


            all_fit_some_triangle = True
            for c in corners_to_test:
                fit_some_triangle = False
                for tri in triangulation:
                    if tri.contains(c):
                        fit_some_triangle = True
                        break
                if not fit_some_triangle:
                    all_fit_some_triangle = False
                    break

            if all_fit_some_triangle:
                print(f'Corners {p1=} {p2=} pass. Size: {abs(p1.x - p2.x + 1) * abs(p1.y - p2.y + 1)}')
                acceptable_corners.append((p1, p2))
    
    best = -1
    for p1, p2 in acceptable_corners:
        area = abs(p1.x - p2.x + 1) * abs(p1.y - p2.y + 1)
        if area > best:
            best = area
    print(f"{best=}")


def solve_2v2(path: str):
    points = read_input(path)
    segments_all = [Segment(p1, p2) for p1, p2 in zip(points, points[1:] + [points[0]])]
    triangulation = triangulate_ears(points)
    round_1_good = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = points[i]
            p2 = points[j]
 
            # 1 - 2
            # |   |
            # 4 - 3
            corners = [
                Point(min(p1.x, p2.x), min(p1.y, p2.y)), # 1
                Point(max(p1.x, p2.x), min(p1.y, p2.y)), # 2
                Point(max(p1.x, p2.x), max(p1.y, p2.y)), # 3
                Point(min(p1.x, p2.x), max(p1.y, p2.y)), # 4
            ]
            segments_cur = [Segment(p1, p2) for p1, p2 in zip(corners, corners[1:] + [corners[0]])]
            
            is_good = True
            for cur_seg in segments_cur:
                
                any_intersection = False
                for ref_seg in segments_all:
                    if cur_seg.intersects_exclusive(ref_seg):
                        any_intersection = True
                        break
                if any_intersection:
                    is_good = False
                    break
            
            if is_good:
                round_1_good.append((p1, p2))

    round_2_good = []
    for p1, p2 in round_1_good:
        corners_to_test = [
            Point(min(p1.x, p2.x), min(p1.y, p2.y)),
            Point(min(p1.x, p2.x), max(p1.y, p2.y)),
            Point(max(p1.x, p2.x), min(p1.y, p2.y)),
            Point(max(p1.x, p2.x), max(p1.y, p2.y)),
        ]


        all_fit_some_triangle = True
        for c in corners_to_test:
            fit_some_triangle = False
            for tri in triangulation:
                if tri.contains(c):
                    fit_some_triangle = True
                    break
            if not fit_some_triangle:
                all_fit_some_triangle = False
                break
        if all_fit_some_triangle:
            round_2_good.append((p1, p2))
    
    round_3_good = []
    for p1, p2 in round_2_good:
        contains_any_segment = False
        for seg in segments_all:
            if p1.area(p2) == 18 and rec_contains_seg(p1, p2, seg):
                print(f"We fucked up: {p1=} {p2=} {seg=} ")
            if rec_contains_seg(p1, p2, seg):
                contains_any_segment = True
                break
        if not contains_any_segment:
            round_3_good.append((p1, p2))

    best = max(round_3_good, key=lambda x: x[0].area(x[1]))
    print(best, best[0].area(best[1]))
    # print('ROUND 1')
    # for p1, p2 in round_1_good:
    #     print(f'{p1=} {p2=} {p1.area(p2)=}')
    
    # print('ROUND 2')
    # for p1, p2 in round_2_good:
    #     print(f'{p1=} {p2=} area: {p1.area(p2)=}')

    # print('ROUND 3')
    # for p1, p2 in round_3_good:
    #     print(f'{p1=} {p2=} area: {p1.area(p2)=}')

if __name__ == '__main__':
    solve_2v2('data/prob-9-test.txt')
    # p1=Point(x=7, y=6) 
    # p2=Point(x=2, y=8) 
    # seg=Segment(p1=Point(x=4, y=6), p2=Point(x=7, y=6)) 
    # rec_contains_seg(p1, p2, seg)