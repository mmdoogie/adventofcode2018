from functools import total_ordering
from Djikstra import Djikstra

with open('data/aoc-2018-15.txt') as f:
    dat = [x.strip('\n') for x in f.readlines()]

@total_ordering
class unit():
    def __init__(self, x, y, kind, ap = 3, hp = 200):
        self._hc = f'{kind}@{x},{y}'
        self.x = x
        self.y = y
        self.kind = kind
        self.ap = ap
        self.hp = hp

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._hc == other._hc

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        else:
            return self.y < other.y

    def __repr__(self):
        return self.kind + '@' + str(self.x) + ',' + str(self.y) + '[' + str(self.hp) + ']'

    def __hash__(self):
        return hash(self._hc)

def parse_dat(elf_power = 3):
    spaces = {}
    units = set()
    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            if c == '#':
                continue
            spaces[(x, y)] = True
            if c == 'E':
                units.add(unit(x, y, c, ap = elf_power))
            elif c == 'G':
                units.add(unit(x, y, c))
    return units, spaces

def move_order(units, already_moved):
    movable = [u for u in units if u not in already_moved]
    return sorted(list(movable))

def find_unit(units, x, y):
    mu = [u for u in units if u.x == x and u.y == y]
    if len(mu) == 0:
        return False
    else:
        return mu[0]

def adj_targets(unit, units, spaces):
    x, y = unit.x, unit.y
    adj = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    tgt = [uu for uu in [find_unit(units, a[0], a[1]) for a in adj] if uu and uu.kind != unit.kind]
    return sorted(tgt, key=lambda x:1000000*x.hp+1000*x.y+x.x)

def make_adj(unit, units, spaces):
    adj = {}
    for s in spaces.keys():
        if (unit.x != s[0] or unit.y != s[1]) and find_unit(units, s[0], s[1]):
            adj[s] = []
        else:
            x, y = s
            ngh_pos = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            adj[s] = sorted([n for n in ngh_pos if n in spaces], key=lambda x:1000*x[1]+x[0])
    return adj

def viz(weights, unit, units, spaces, path = [], elf_power = 3):
    print(chr(27) + '[H')
    min_x = min([k[0] for k in spaces.keys()])
    max_x = max([k[0] for k in spaces.keys()])
    min_y = min([k[1] for k in spaces.keys()])
    max_y = max([k[1] for k in spaces.keys()])
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            uu = find_unit(units, x, y)
            if unit.x == x and unit.y == y:
                print(f'{unit.kind*2} ', end='')
            elif (x, y) in weights and uu:
                print(f'{weights[(x,y)]:02d}{uu.kind}', end='')
            elif uu:
                print(f'U{uu.kind} ', end='')
            elif (x, y) in path:
                print(f'{path.index((x, y)):02d} ', end='')
            elif (x, y) in spaces:
                print('__ ', end='')
            else:
                print('   ', end='')
        print()
    print('Elves:', len([u for u in units if u.kind == 'E']), 'Gnomes:', len([u for u in units if u.kind == 'G']), end='          \n')
    print('Elf Power:', elf_power)

def closest(weights, unit, units):
    act_weights = {k: v for k, v in weights.items() if (uu := find_unit(units, k[0], k[1])) and uu != unit and uu.kind != unit.kind}
    order = sorted(act_weights.items(), key=lambda x: x[1])
    cand = [o for o in order if o[1] == order[0][1]]
    order = sorted(cand, key=lambda x: 1000*x[0][1] + x[0][0])
    if len(order) == 0:
        return None
    else:
        return order[0][0]

def play_game(output = True, elf_power = 3, end_at_first_loss = False):
    units, spaces = parse_dat(elf_power = elf_power)
    start_elves = len([u for u in units if u.kind == 'E'])

    rounds_complete = 0
    already_moved = set()
    while True:
        order = move_order(units, already_moved)
        o = order[0]
        if len([u for u in units if u.kind != o.kind]) == 0:
            if output:
                print('winner found in round:', rounds_complete + 1)
            break
        targets = adj_targets(o, units, spaces)
        if len(targets) == 0:
            ngh = make_adj(o, units, spaces)
            weights, paths = Djikstra(ngh, (o.x, o.y))
            move_tgt = closest(weights, o, units)
            if move_tgt is not None:
                move_path = paths[move_tgt]
                if output:
                    viz(weights, o, units, spaces, move_path, elf_power)
                o.x = move_path[1][0]
                o.y = move_path[1][1]
            else:
                if output:
                    viz(weights, o, units, spaces, elf_power = elf_power)
        already_moved.add(o)
        targets = adj_targets(o, units, spaces)
        if len(targets) != 0:
            if output:
                viz(weights, o, units, spaces, elf_power = elf_power)
            targets[0].hp -= o.ap
            if targets[0].hp <= 0:
                if targets[0].kind == 'E' and end_at_first_loss:
                    return 0, 1
                units.remove(targets[0])
                if targets[0] in already_moved:
                    already_moved.remove(targets[0])

        if len(already_moved) == len(units):
            rounds_complete += 1
            if output:
                viz(set(), o, units, spaces, elf_power = elf_power)
                print('rounds  complete:', rounds_complete)
            already_moved = set()

    final_elves = len([u for u in units if u.kind == 'E'])
    return rounds_complete * sum([u.hp for u in units]), start_elves - final_elves

def part1(output = True):
    if output:
        print(chr(27) + '[H' + chr(27) + '[J')
    score, elves_lost = play_game(output)
    return score

def part2(output = True):
    elf_power = 4
    while True:
        if output:
            print(chr(27) + '[H' + chr(27) + '[J')
        score, elves_lost = play_game(output, elf_power = elf_power, end_at_first_loss = True)
        if elves_lost == 0:
            return score
        elf_power += 1
