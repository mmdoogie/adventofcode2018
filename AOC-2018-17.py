import re
import time

with open('data/aoc-2018-17.txt') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    rx = re.compile('([xy])=([0-9]+), ([xy])=([0-9]+)..([0-9]+)')
    clay = {}
    for d in dat:
        m = rx.match(d).groups()
        if m[0] == 'x':
            x = int(m[1])
            assert m[2] == 'y'
            for y in range(int(m[3]), int(m[4])+1):
                clay[(x, y)] = True
        else:
            assert m[0] == 'y' and m[2] == 'x'
            y = int(m[1])
            for x in range(int(m[3]), int(m[4]) + 1):
                clay[(x, y)] = True

    return clay

def print_section(clay, dx, dy, max_y):
    print(chr(27) + '[H')
    print(' '*120 + 'v--' + f'{dx:04d}')
    for y in range(dy - 25, dy + 25):
        for x in range(dx - 120, dx + 120):
            if y > max_y:
                print('=', end = '')
            elif x == dx and y == dy:
                print('o', end = '')
            elif (x, y) in clay:
                print('#', end = '')
            else:
                print(' ', end = '')
        print(f'[{y:04d}]', '**' if y == dy else '')
    time.sleep(0.01)

def drip(drip_x, drip_y, clay, visited, min_y, max_y, output):
    if (drip_x, drip_y + 1) in visited:
        return
    drop_x, drop_y = drip_x, drip_y
    while (drop_x, drop_y + 1) not in clay:
        drop_y += 1
        if drop_y >= min_y and drop_y <= max_y:
            visited.add((drop_x, drop_y))
            if output:
                print_section(clay, drop_x, drop_y, max_y)
        if drop_y > max_y:
            return

    fill_y = drop_y
    while True:
        visited.add((drop_x, fill_y))
        if output:
            print_section(clay, drop_x, fill_y, max_y)

        new_lvl = [(drop_x, fill_y)]
        left_x = drop_x
        left_fall = None
        while (left_x - 1, fill_y) not in clay:
            left_x -= 1
            new_lvl += [(left_x, fill_y)]
            visited.add((left_x, fill_y))
            if (left_x, fill_y + 1) not in clay:
                left_fall = (left_x, fill_y)
                break

        right_x = drop_x
        right_fall = None
        while (right_x + 1, fill_y) not in clay:
            right_x += 1
            new_lvl += [(right_x, fill_y)]
            visited.add((right_x, fill_y))
            if (right_x, fill_y + 1) not in clay:
                right_fall = (right_x, fill_y)
                break

        if left_fall is not None or right_fall is not None:
            break

        for n in new_lvl:
            clay[n] = True
        if output:
            print(len(visited))
        fill_y -= 1

    if left_fall is not None:
        drip(*left_fall, clay, visited, min_y, max_y, output)

    if right_fall is not None:
        drip(*right_fall, clay, visited, min_y, max_y, output)

clay_change = 0

def part1(output = True):
    global clay_change

    clay = parse()
    spring = (500, 0)
    visited = set()
    min_y = min(clay.keys(), key = lambda x: x[1])[1]
    max_y = max(clay.keys(), key = lambda x: x[1])[1]

    if output:
        print(chr(27) + '[2J')

    pre_clay = len(clay)
    drip(*spring, clay, visited, min_y, max_y, output)
    post_clay = len(clay)
    clay_change = post_clay - pre_clay

    return len(visited)

def part2(output = True):
    global clay_change

    return clay_change

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
