import re
from itertools import takewhile
from functools import reduce
from operator import mul

nums = [x for x in range(0,10)]

symbols = set()
gear_symbols = set()

def assign_symbol_positions(matrix):
    global symbols
    regex_pattern = re.compile(r'[0-9]|\.')
    for y, row in enumerate(matrix):
        for x, position in enumerate(row.strip()):
            if not re.match(regex_pattern, position):
                symbols.add((x,y))


def assign_gear_symbols(matrix):
    global gear_symbols 
    regex_pattern = re.compile(r'\*')
    for y, row in enumerate(matrix):
        for x, position in enumerate(row.strip()):
            if re.match(regex_pattern, position):
                gear_symbols.add((x,y))


def is_valid(num_coords, y_coord, max_x, max_y):
    dummy_val = list(num_coords)[0][0]
    num_min_x, num_max_x = reduce(lambda acc, a: (min(acc[0], a[0]), max(acc[1], a[0])), num_coords ,(dummy_val, dummy_val))
    neighbours_range_x = {x for x in range(num_min_x - 1 , num_max_x + 2) if 0 <= x <= max_x}
    neighbours_range_y = {y for y in range(y_coord - 1, y_coord + 2) if 0 <= y <= max_y}
    neighbours_coords = {(x,y) for x in neighbours_range_x for y in neighbours_range_y if (x,y) not in num_coords}
    
    return not symbols.isdisjoint(neighbours_coords)


def solve_a(matrix):
    max_x = len(matrix[0])
    max_y = len(matrix)
    regex_pattern = re.compile(r'[0-9]')
    searched = set()
    nums = []
    for y, line in enumerate(matrix):
        for x, char in enumerate(line):
            if (x-1 > 0 and regex_pattern.match(line[x-1])) or not regex_pattern.match(char) or (x,y) in  searched:
                continue
            z = [*range(x, x + len(list(takewhile(lambda a: regex_pattern.match(a) , line[x:]))))]
            num_coords = {(x,y) for x in z}
            searched |= num_coords

            num = line[min(z):max(z)+1]

            valid = is_valid(num_coords, y, max_x, max_y)
            searched |= num_coords
            if valid:
                nums.append(int(''.join(num)))

    return sum(nums)


def adjacent_coords(matrix, coord):
    x_coords = {coord[0] + x for x in range(-1,2) if 0 <= coord[0] + x < len(matrix[0])}
    y_coords = {coord[1] + y for y in range(-1,2) if 0 <= coord[1] + y < len(matrix)}
    return {(x,y) for x in x_coords for y in y_coords if (x,y) != coord}


def solve_b(matrix):
    max_x = len(matrix[0])
    max_y = len(matrix)
    regex_pattern = re.compile(r'[0-9]')
    searched = set()
    nums = dict()
    for y, line in enumerate(matrix):
        for x, char in enumerate(line):
            if (x-1 > 0 and regex_pattern.match(line[x-1])) or not regex_pattern.match(char) or (x,y) in  searched:
                continue
            z = [*range(x, x + len(list(takewhile(lambda a: regex_pattern.match(a) , line[x:]))))]
            num_coords = {(x,y) for x in z}
            searched |= num_coords

            num = int(line[min(z):max(z)+1])

            valid = is_valid(num_coords, y, max_x, max_y)
            searched |= num_coords
            if valid:
                all_coords = set()
                for coord in num_coords:
                    pass
                    all_coords.update(adjacent_coords(matrix, coord))
                for coord in all_coords:
                    nums[coord] = [num] if coord not in nums else [num, *nums[coord]]

    add_list = []
    for gear_symbol in gear_symbols:
        if gear_symbol in nums and len(nums[gear_symbol]) == 2:
            add_list.append(reduce(mul, nums[gear_symbol], 1))
    return sum(add_list)


with open('day3/input.csv') as file:
    lines = file.readlines()

    assign_symbol_positions(lines)
    ans_a = solve_a(lines)
    print(f'Answer for A:\t', ans_a)

    assign_gear_symbols(lines)
    ans_b = solve_b(lines)
    print(f'Answer for B:\t', ans_b)
