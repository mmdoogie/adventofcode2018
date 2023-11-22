import argparse

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

    try:
        day_module = __import__(day_module_name)
    except Exception as ex:
        print(f'Day {day_str} not found or error running: {ex}')
        return

    if day_num in result_module.results:
        results = result_module.results[day_num]
    else:
        results = None

    try:
        part1_val = day_module.part1(args.o)
        if results is not None and 1 in results:
            print(f'Day {day_str}, Part 1:', f'{part1_val:<35}', f'{results[1]:<35}', 'PASS' if results[1] == part1_val else 'FAIL')
        else:
            print(f'Day {day_str}, Part 1:', f'{part1_val:<35}')
    except Exception as ex:
        print(f'Day {day_str}, Part 1: Not found or error running: {ex}')

    try:
        part2_val = day_module.part2(args.o)
        if results is not None and 2 in results:
            print(f'Day {day_str}, Part 2:', f'{part2_val:<35}', f'{results[2]:<35}', 'PASS' if results[2] == part2_val else 'FAIL')
        else:
            print(f'Day {day_str}, Part 2:', f'{part2_val:<35}')
    except Exception as ex:
        print(f'Day {day_str}, Part 2: Not found or error running: {ex}')

if args.d == 0:
    args.o = False
    for day_num in range(1, 26):
        run_day(day_num)
else:
    run_day(args.d)
