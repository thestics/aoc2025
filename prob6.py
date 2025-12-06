from functools import reduce
from dataclasses import dataclass
from typing import Literal


def solve_1():
    with open('data/prob6.txt') as f:
        data = f.read()
    
    struc = []
    for line in data.split('\n'):
        items = [x for x in line.split()]
        struc.append(items)
    
    transposed = list(zip(*struc))

    total = 0
    for row in transposed:
        op = row[-1]
        if op == '+':
            total += reduce(lambda acc, cur: int(acc) + int(cur), row[:-1])
        elif op == '*':
            total += reduce(lambda acc, cur: int(acc) * int(cur), row[:-1])
    print(f'{total=}')



@dataclass
class Block:
    op: Literal['+', '*']
    contents: list

    def solve(self):
        nums = [int(''.join([ch for ch in cur_num if ch]).strip()) for cur_num in self.contents]
        print(nums)
        if self.op == '+':
            return reduce(lambda acc, val: acc + val, nums)
        else:
            return reduce(lambda acc, val: acc * val, nums)


def solve_2():
    with open('data/prob6.txt') as f:
        data = [list(row[:-1]) for row in f.readlines()]
    transposed = [x for x in list(zip(*data)) if ''.join(x).strip()]

    blocks = []
    cur_block = None
    for row in transposed:
        print(row)
        if row[-1] in ('+', '*'):
            if cur_block is not None:
                blocks.append(cur_block)

            cur_block = Block(op=row[-1], contents=[row[:-1]])
        else:
            cur_block.contents.append(row[:-1])
    blocks.append(cur_block)
    print(blocks)

    total = 0
    for b in blocks:
        total += b.solve()
    print(f'{total=}')


solve_2()