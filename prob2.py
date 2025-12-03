from pprint import pprint


def is_silly(num: str):
    for i in range(len(num) - 1):
        size = i + 1
        if len(num) % size != 0:
            continue

        slice = num[0: i + 1]
        factor = len(num) // size
        candidate = slice * factor
        # print(f"{i=} {slice=} {candidate=} {num=}")
        if candidate == num:
            return True
    return False


def is_silly_half(num: str):
    if len(num) % 2 != 0:
        return False
    
    return num[:len(num)//2] == num[len(num)//2:]


def main():
    with open('data/prob2.txt') as f:
        data = f.read()
    ranges = data.split(',')
    ranges = [x.split('-') for x in ranges]
    
    total_matches = []
    for r in ranges:
        cur_matches = []
        start, stop = r

        for i in range(int(start), int(stop) + 1):
            num = str(i)
            # if is_silly_half(num):
            if is_silly(num):
                cur_matches.append(num)
        print(f'{r=} {cur_matches=}')
        total_matches.extend(cur_matches)
    return sum(int(x) for x in total_matches)



if __name__ == "__main__":
    res = main()
    print(res)
    # print(f"{is_silly('22')=}")
    # print(f"{is_silly('1010')=}")
    # print(f"{is_silly('1011')=}")
    # print(f"{is_silly('38593859')=}")
