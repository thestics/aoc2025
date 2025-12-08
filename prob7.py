def solve1():
    def print_board():
        for row in chars:
            print("".join(row))
        print()

    chars = []
    with open("data/prob-7.txt") as f:
        for row in f.readlines():
            chars.append(list(row)[:-1])

    # print_board()

    splits = 0
    for i in range(len(chars)):
        # print(f"{i=}")
        # print_board()

        for j in range(len(chars[0])):
            if chars[i][j] == "S":
                chars[i + 1][j] = "|"
            elif chars[i][j] == "^" and chars[i - 1][j] == "|":
                splits += 1
                k = i
                left_unblocked = True
                right_unblocked = True
                while k < len(chars) and (left_unblocked or right_unblocked):
                    # chars[k][j - 1] != "^" or chars[k][j + 1] != "^"
                    left_unblocked = left_unblocked and chars[k][j - 1] != "^"
                    right_unblocked = right_unblocked and chars[k][j + 1] != "^"
                    if left_unblocked:
                        chars[k][j - 1] = "|"
                    if right_unblocked:
                        chars[k][j + 1] = "|"
                    k += 1

    print_board()
    print(f"{splits=}")


def solve2():
    def print_board():
        for row in chars:
            print(row)
        print()

    def celltoint(x):
        assert x == "." or isinstance(x, int), x
        if x == ".":
            return 0
        return x

    chars = []
    with open("data/prob-7.txt") as f:
        for row in f.readlines():
            chars.append(list(row)[:-1])

    # init
    chars[1][chars[0].index("S")] = 1
    width = len(chars[0])
    height = len(chars)

    # print_board()
    for i in range(2, height):
        for j in range(width):
            # if not-fillable or blocked from the top
            if chars[i][j] != "." or chars[i - 1][j] == "^":
                continue

            above = celltoint(chars[i - 1][j])
            above_left = 0
            above_right = 0
            if j >= 1 and chars[i][j - 1] == "^":
                above_left = celltoint(chars[i - 1][j - 1])
            if j <= width - 2 and chars[i][j + 1] == "^":
                above_right = celltoint(chars[i - 1][j + 1])
            total = above + above_left + above_right

            chars[i][j] = total
            if i <= height - 1:
                chars[i + 1][j] = total
    res = sum([celltoint(x) for x in chars[-1]])
    print_board()
    print(f"{res=}")


if __name__ == "__main__":
    solve2()
