with open('data/aoc-2018-10.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def min_pos(pos):
    min_x = min(pos, key=lambda x: x[0])[0]
    min_y = min(pos, key=lambda x: x[1])[1]

    return (min_x, min_y)

def max_pos(pos):
    max_x = max(pos, key=lambda x: x[0])[0]
    max_y = max(pos, key=lambda x: x[1])[1]

    return (max_x, max_y)

def area_pos(pos):
    min_x, min_y = min_pos(pos)
    max_x, max_y = max_pos(pos)

    return (max_x - min_x) * (max_y - min_y)

def find_msg(output = True):
    pos = [[int(x) for x in d.split('> ')[0].split('<')[1].split(',')] for d in dat]
    vel = [[int(x) for x in d.split('y=<')[1].split('>')[0].split(',')] for d in dat]

    min_area = area_pos(pos)
    min_it = 0

    it = 0
    while True:
        it += 1
        for i in range(len(pos)):
            pos[i][0] += vel[i][0]
            pos[i][1] += vel[i][1]
        a = area_pos(pos)
        if a < min_area:
            if output:
                print('Step:', it, 'Area:', a)
            min_area = a
            min_it = it
        if it - min_it >= 1:
            break
    
    for i in range(len(pos)):
        pos[i][0] -= vel[i][0]
        pos[i][1] -= vel[i][1]
    assert area_pos(pos) == min_area

    min_x, min_y = min_pos(pos)
    max_x, max_y = max_pos(pos)

    lines = ['']
    for y in range(min_y, max_y + 1):
        line = ''
        for x in range(min_x, max_x + 1):
            if [x, y] in pos:
                line += '##'
            else:
                line += '  '
        lines += [line]
    lines += ['']

    return '\n'.join(lines), it - 1

def part1(output = True):
    global msg_time
    txt, msg_time = find_msg(output)
    
    return txt

def part2(output = True):
    global msg_time

    return msg_time
