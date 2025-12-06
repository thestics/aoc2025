from pprint import pprint


def read_input():
    with open("data/prob4.txt") as f:
        data = [list(row) for row in f.read().split("\n")]
    return data


def remove_one_round(data: list[list[str]]):
    vert_size = len(data)
    horiz_size = len(data[0])

    total = 0
    for i in range(vert_size):
        for j in range(horiz_size):
            next_idxs = [
                (m, n)
                for m in range(i - 1, i + 2)
                for n in range(j - 1, j + 2)
                if 0 <= m <= vert_size - 1
                and 0 <= n <= horiz_size - 1
                and (m, n) != (i, j)
            ]
            neighbours_count = [data[m][n] for m, n in next_idxs].count("@")
            # That is not exactly the same as in the problem statement, because by counting
            # and removing blocks at the same time you might free up rolls downstream
            # which wouldn't have been free before.
            # Counter argument is as follows: if by removing roll you accidentally unblock
            # another roll and specifically do not remove it this round -- you would end up
            # coming across it and removing it in the following round anyway.
            # Hence, while number of rolls freed per round might differ from the one in the
            # simple test case the full solution should still match
            if neighbours_count < 4 and data[i][j] == "@":
                total += 1
                data[i][j] = "."
    return total


def solve_v1():
    data = read_input()

    vert_size = len(data)
    horiz_size = len(data[0])

    total = 0
    for i in range(vert_size):
        for j in range(horiz_size):
            next_idxs = [
                (m, n)
                for m in range(i - 1, i + 2)
                for n in range(j - 1, j + 2)
                if 0 <= m <= vert_size - 1
                and 0 <= n <= horiz_size - 1
                and (m, n) != (i, j)
            ]
            neighbours_count = [data[m][n] for m, n in next_idxs].count("@")
            if neighbours_count < 4 and data[i][j] == "@":
                total += 1
                print(f"{i=} {j=} {next_idxs=} {neighbours_count=} COUNTED")
            print(f"{i=} {j=} {next_idxs=} {neighbours_count=}")

    print(f"{total=}")


def solve_v2():
    data = read_input()

    changed = 1
    total = 0
    round = 0
    while changed:
        changed = remove_one_round(data)
        total += changed
        round += 1
        print(f"{round=} {changed=}")
    print(f"{total=}")


if __name__ == "__main__":
    # solve_v1()
    solve_v2()
