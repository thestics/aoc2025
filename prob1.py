

if __name__ == '__main__':
    with open('data/prob1.txt') as f:
        data = f.readlines()
    
    modulo = 100
    cur = 50

    total = 0

    for i, line in enumerate(data):
        was_zero = cur == 0
        direction = line[0]
        count = int(line[1:].strip())
        # print(f'{direction=} {count=}')

        clicks = 0
        if direction == 'L':
            new = cur - count
            cur = new % modulo
        elif direction == 'R':
            new = cur + count
            cur = new % modulo
        else:
            assert False, 'Unreachable'


        clicks = 0
        if new == 0:
            clicks = 1
        else:
            clicks = abs(new // modulo)

        if was_zero and clicks > 0:
            clicks -= 1
    
        total += clicks
            
        click_str = f'{clicks=}'
        print(f'{i=} {line.strip()}: {cur=} {new=} {click_str if clicks else ""}')
    print(f'Code = {total}')
