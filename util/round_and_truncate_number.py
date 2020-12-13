"""
Based on https://realpython.com/python-rounding/
"""

import math


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def round_half_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier - 0.5) / multiplier


def round_half_away_from_zero(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return math.copysign(rounded_abs, n)


if __name__ == '__main__':
    numbers = (12.3456789, -12.3456789)
    testing_range = range(-5, 5+1)

    print(f'Given numbers: {numbers}')
    print(f'Test functions in next range (passed as `decimals` argument): {testing_range}')

    # todo print in table representation
    def test(func):
        print(f'\nTest {func.__name__}():')
        for number in numbers:
            for n_digits in testing_range:
                print(func(number, n_digits))

    test(truncate)
    test(round_up)
    test(round_down)
    test(round_half_up)
    test(round_half_down)
    test(round_half_away_from_zero)

    import builtins
    test(builtins.round)
