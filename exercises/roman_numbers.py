from collections import namedtuple
import pytest

# https://en.wikipedia.org/wiki/Roman_numerals
# http://ph0enix.ru/romannums/

Map = namedtuple('Map', 'arabic roman')

# Ascendant order!
#   First four rows for the arabic numbers form the logic pattern.
#   1, 4, 5, 9. Next arabic numbers consist of these numbers + n zeros.
#   10, 40, 50, 90.
#   In current implementation the main accent is on the mapping structure,
#     not the final algorithm.

mapping = (
    (1, 'I'),
    (4, 'IV'),
    (5, 'V'),
    (9, 'IX'),

    (10, 'X'),
    (40, 'XL'),
    (50, 'L'),
    (90, 'XC'),

    (100, 'C'),
    (400, 'CD'),
    (500, 'D'),
    (900, 'CM'),

    (1000, 'M'),
)
# Convert inner tuples to named tuples.
mapping = tuple(map(lambda i: Map(*i), mapping))


def arabic_to_roman(x):
    assert 0 < x < 4000

    i = len(mapping) - 1  # Last index of the `mapping`.
    result = []

    while i >= 0 and x > 0:

        while True:

            arabic = mapping[i].arabic
            roman = mapping[i].roman

            if x // arabic > 0:
                x -= arabic
                result.append(roman)

            else:
                break

        i -= 1

    return ''.join(result)


def roman_to_arabic(x):
    assert isinstance(x, str)

    result = 0
    previous = None

    for letter in reversed(x):

        for pair in mapping:
            if pair.roman == letter:
                current = pair.arabic
                break
        else:
            raise IndexError('Roman letter {} was not found in mapping.'.format(letter))

        if previous and previous > current:
            result -= current
        else:
            result += current

        previous = current

    return result


tests = [
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V'),
    (6, 'VI'),
    (7, 'VII'),
    (8, 'VIII'),
    (9, 'IX'),
    (10, 'X'),
    (11, 'XI'),
    (14, 'XIV'),
    (15, 'XV'),
    (19, 'XIX'),
    (20, 'XX'),
    (49, 'XLIX'),
    (50, 'L'),
    (51, 'LI'),
    (98, 'XCVIII'),
    (99, 'XCIX'),
    (3999, 'MMMCMXCIX'),
]

reversed_tests = [(i[1], i[0]) for i in tests]


@pytest.mark.parametrize('input,expected_output', tests)
def test_arabic_to_roman(input, expected_output):
    assert arabic_to_roman(input) == expected_output


@pytest.mark.parametrize('input,expected_output', reversed_tests)
def test_roman_to_arabic(input, expected_output):
    assert roman_to_arabic(input) == expected_output


pytest.main(['-q', '--tb=line', __file__])
