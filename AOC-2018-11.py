with open('data/aoc-2018-11.txt') as f:
    dat = int([x.strip() for x in f.readlines()][0])

def power_level(sn, cell):
    x, y = cell
    rack_id = x + 10
    power_level = ((((rack_id * y) + sn) * rack_id) // 100) % 10
    return power_level - 5

def part1(output = True):
    if output:
        assert power_level(8, (3, 5)) == 4
        assert power_level(57, (122, 79)) == -5
        assert power_level(39, (217, 196)) == 0
        assert power_level(71, (101, 153)) == 4

    levels = {}
    for y in range(1, 301):
        for x in range(1, 301):
            levels[(x, y)] = power_level(dat, (x, y))

    max_level = 0
    max_pt = (0, 0)
    for y in range(1, 301 - 2):
        for x in range(1, 301 - 2):
            pts = [(x, y    ), (x + 1, y    ), (x + 2, y    ),
                   (x, y + 1), (x + 1, y + 1), (x + 2, y + 2),
                   (x, y + 2), (x + 1, y + 2), (x + 2, y + 2)]
            total_level = sum([levels[p] for p in pts])
            if total_level > max_level:
                if output:
                    print(f'At {x},{y} level={total_level}')
                max_level = total_level
                max_pt = (x, y)

    return ','.join([str(v) for v in max_pt])

def part2(output = True):
    levels = {}
    for y in range(1, 301):
        for x in range(1, 301):
            levels[(x, y)] = power_level(dat, (x, y))

    max_level = 0
    max_pt = (0, 0, 0)
    for y in range(1, 301 - 2):
        for x in range(1, 301 - 2):
            total_level = 0
            for dy in range(3):
                for dx in range(3):
                    total_level += levels[(x + dx, y + dy)]
            if total_level > max_level:
                if output:
                    print(f'At {x},{y},3 level={total_level}')
                max_level = total_level
                max_pt = (x, y, 3)
            while True:
                if x + dx + 1 > 300 or y + dy + 1 > 300:
                    break
                for ddy in range(dy):
                    total_level += levels[(x + dx + 1, y + ddy)]
                for ddx in range(dx):
                    total_level += levels[(x + ddx, y + dy + 1)]
                total_level += levels[(x + dx + 1, y + dy + 1)]
                if total_level > max_level:
                    if output:
                        print(f'At {x},{y},{dx + 2} level={total_level}')
                    max_level = total_level
                    max_pt = (x, y, dx + 2)
                dx += 1
                dy += 1

    return ','.join([str(v) for v in max_pt])
