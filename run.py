import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument('-d', type = int, required = True, help = 'Day to run. 0 for all.')
ap.add_argument('-o', action = 'store_true', help = 'Show optional output')
args = ap.parse_args()

if args.d < 0 or args.d > 35:
    print('Day must be between 1 and 35 inclusive.  Use 0 for all')
    exit(1)

result_module_name = 'data.results'
result_module = __import__(result_module_name).results

def run_day(day_num):
    day_str = f'{day_num:02d}'
    day_module_name = f'AOC-2018-{day_str}'
    passing = [False, False]
    total_time = 0

    try:
        day_module = __import__(day_module_name)
    except Exception as ex:
        print(f'Day {day_str} not found or error running: {ex}')
        return 0, 0

    if day_num in result_module.results:
        results = result_module.results[day_num]
    else:
        results = None

    try:
        t_before = time.process_time()
        part1_val = day_module.part1(args.o)
        t_after = time.process_time()
        dt = round(t_after - t_before, 3)
        total_time += dt
        print(f'[{dt:>7.3f}] ', end='')
        if results is not None and 1 in results:
            if 'no_match' not in results or 1 not in results['no_match']:
                passing[0] = (results[1] == part1_val)
                print(f'Day {day_str}, Part 1:', f'{part1_val:<35}', f'{results[1]:<35}', 'PASS' if passing[0] else 'FAIL')
            else:
                passing[0] = True
                print(f'Day {day_str}, Part 1:', f'{part1_val:<35}', f'expecting: {results[1]:<35}')
        else:
            print(f'Day {day_str}, Part 1:', f'{part1_val:<35}')
    except Exception as ex:
        print(f'Day {day_str}, Part 1: Not found or error running: {ex}')

    try:
        t_before = time.process_time()
        part2_val = day_module.part2(args.o)
        t_after = time.process_time()
        dt = round(t_after - t_before, 3)
        total_time += dt
        print(f'[{dt:>7.3f}] ', end='')
        if results is not None and 2 in results:
            if 'no_match' not in results or 2 not in results['no_match']:
                passing[1] = (results[2] == part2_val)
                print(f'Day {day_str}, Part 2:', f'{part2_val:<35}', f'{results[2]:<35}', 'PASS' if passing[1] else 'FAIL')
            else:
                passing[1] = True
                print(f'Day {day_str}, Part 2:', f'{part2_val:<35}', f'expecting: {results[2]:<35}')
        else:
            print(f'Day {day_str}, Part 2:', f'{part2_val:<35}')
    except Exception as ex:
        print(f'Day {day_str}, Part 2: Not found or error running: {ex}')

    return sum(passing), total_time

if args.d == 0:
    args.o = False
    results = [run_day(day_num) for day_num in range(1, 26)]
    passing = sum([r[0] for r in results])
    total_time = sum([r[1] for r in results])
    print(f'[{total_time:>7.3f}] Passing:', passing, 'of 50')
else:
    run_day(args.d)
