def max_jolt(line: str):
    mx = 0
    for i in range(len(line)):
        for j in range(i + 1, len(line)):
            val = int(f"{line[i]}{line[j]}")
            if val > mx:
                mx = val
    return mx


def sorted_suffixes(data: str):
    data_wi = list(enumerate(data))

    sorted_subsets = [None for i in range(len(data_wi))]
    for i in range(len(data_wi)):
        sorted_subsets[i] = sorted(data_wi[i:], key=lambda x: x[1], reverse=True)

    return sorted_subsets
    # for i in range(len(data)):
    #     print(f"({i=: >2}, a[i]={data[i]}): {sorted_subsets[i]}")


def print_precalc(precalc):
    for i in range(len(precalc)):
        print(
            f"({i=: >2}, a[i]={data[i]}): {', '.join([f"({idx: >2}, {val: >2})" for idx, val in precalc[i]])}"
        )


def max_jolt_with_sorted_subsets(data: list[str], k: int):
    precalc = sorted_suffixes(data)
    # print_precalc(precalc)
    pointers = [i for i in range(len(data) - k, len(data))]

    prev_lookup_idx = -1
    for i in range(len(pointers)):
        pi = pointers[i]
        lookup_seq = precalc[prev_lookup_idx + 1]

        for idx, val in lookup_seq:
            if idx > pi:
                continue
            pointers[i] = idx
            prev_lookup_idx = idx
            break

    # print(pointers)
    # print(s)
    s = "".join([data[p] for p in pointers])
    return s


def solve():
    with open("data/prob3.txt") as f:
        data = f.read()

    total = 0
    for i, line in enumerate(data.split("\n")):
        v = max_jolt(line)
        print(f"i={i:2} {line=} {v=}")
        total += v
    print(f"{total=}")


def solve_v2():
    with open("data/prob3.txt") as f:
        data = f.read()

    total = 0
    for i, line in enumerate(data.split("\n")):
        v = max_jolt_with_sorted_subsets(line, 12)
        print(f"i={i:2} {line=} {v=}")
        total += int(v)
    print(f"{total=}")


if __name__ == "__main__":
    # main()
    # data = "234234234234278"
    # precalc = sorted_suffixes(data)
    # print(max_jolt_with_sorted_subsets(data, 12))
    solve_v2()
