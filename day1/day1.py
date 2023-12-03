import re
from functools import reduce

nums_a = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
nums_b = {'one' : 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine' : 9, **nums_a }

def calibration_values(input, nums):
    nums_b_regex = '|'.join(nums.keys())
    vals =  re.findall(f'(?=({nums_b_regex}))', input.strip())
    return nums[vals[0]] * 10 + nums[vals[-1]]

with open('day1/a-input.csv') as file:
    file = file.readlines()
    a = reduce(lambda acc, e: acc + calibration_values(e, nums_a), file, 0)
    print(f'answer A: {a}')
    a = reduce(lambda acc, e: acc + calibration_values(e, nums_b), file, 0)
    print(f'answer B: {a}')
