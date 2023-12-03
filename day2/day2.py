import re
from functools import reduce
from operator import mul 

filter_threshold = {'red': 12, 'green': 13, 'blue': 14}

def solve_a(line, filter_threshold):
    game_id, draws= re.search(r'^Game (\d+):(.*)$', line).groups()
    def f(draw):
        cubes_by_color = draw.split(',')
        for elem in cubes_by_color:
            num, color = elem.strip().split()
            if int(num) > filter_threshold.get(color, 0):
                return False
        return True 
    ok = reduce(lambda acc, e: acc and f(e), draws.split(';'), True)
    return int(game_id) if ok else 0

def solve_b(line):
    _, draws= re.search(r'^Game (\d+):(.*)$', line).groups()
    def f(acc, draw):
        cubes_by_color = draw.split(',')
        for elem in cubes_by_color:
            num, color = elem.strip().split()
            clr = acc.get(color, 0)
            acc[color] = max(clr, int(num))
        return acc
    minimum_required = reduce(lambda acc, e: f(acc, e), draws.split(';'), {})
    return reduce(mul, minimum_required.values(), 1)



with open('./day2/input.csv') as file:
    lines = list(map(lambda a: a.strip(), file.readlines()))

    ans_a = reduce(lambda acc, e: acc + solve_a(e, filter_threshold), lines, 0)
    print(f'Answer A: {ans_a}')

    ans_b = reduce(lambda acc, e: acc + solve_b(e), lines, 0)
    print(f"Answer B: {ans_b}")
