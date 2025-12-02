

if __name__ == '__main__':
    with open('data/prob1.txt') as f:
        data = f.readlines()
    
    modulo = 100
    cur = 50

    total = 0

    for i, line in enumerate(data):
        # was_zero = cur == 0
        direction = line[0]
        count = int(line[1:].strip())

        clicks = count // 100 # 1
        count_abs = count % 100 # 50

        # cur 50
        if direction == 'L':
            new = cur - count_abs # 0
            if new < 0:
                if cur != 0:
                    clicks += 1
                cur = 100 - abs(new)
            else:
                cur = new
        elif direction == 'R':
            new = cur + count_abs
            if new >= 100:
                clicks += 1
                cur = new - 100
            else:
                cur = new
        else:
            assert False, 'Unreachable'


        if new == 0:
            clicks += 1

        # if was_zero and clicks > 0:
        #     clicks -= 1
    
        total += clicks
            
        click_str = f'{clicks=}'
        print(f'{i=} {line.strip()}: {cur=} {new=} {click_str if clicks else ""}')
    print(f'Code = {total}')
