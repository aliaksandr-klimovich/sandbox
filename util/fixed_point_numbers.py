"""
Converts Q formatted number to float and visa versa.

To get information about Q number format see wiki:
    https://en.wikipedia.org/wiki/Q_(number_format)
"""

import re


class ConversionError(Exception):
    pass


# data type regex
_r = re.compile('(?P<s>[SU])(?P<m>[0-9]+)Q(?P<e>[0-9]+)')


def float_to_fixed(data_type: str, float_value: float, error_strategy: str = 'raise') -> int:
    """
    Converts float into a fixed representation of a number.

    data_type should contain fixed number type representation.
    First char should be U (unsigned) or S(signed). Next is the number of bits for significand (integer part).
    Next should come the Q char and next is the number of bits for exponent (fractional part).
    Example: S4Q4. Here the number of significand bits is 3, 1 bit is taken by sign. And next 4 bits represent exponent.
    In total here is a 8 bits number.

    :param data_type: String containing data type of the fixed number.
    :param float_value: Float value to convert from.
    :param error_strategy: "raise" or "skip" errors.
        This option influence on how to handle the values that exceed any bound.
        "skip" means that the value outside the valid range will be converted to an extreme value of the range.
        "raise" can raise ConversionError in a similar case.
        Setting this option to "skip" doesn't mean that other exceptions cannot raise.
    """

    if not isinstance(float_value, float):
        raise ConversionError(
            f'Invalid value type. Given value {float_value} of type {type(float_value)} should be of float type.')

    if error_strategy not in ('skip', 'raise'):
        raise ConversionError(f'Invalid error strategy. Given value {error_strategy} is not valid. '
                              f'Valid values are: "skip", "raise".')

    # parse data_type
    match = _r.search(data_type)
    if not match:
        raise ConversionError(f'Invalid data type. '
                              f'Given data type {data_type} should meet the rules. See function description.')

    # get mantissa value, check it later
    m = int(match['m'])  # mantissa

    # get exponent value and check it
    e = int(match['e'])  # exponent

    # get sign value
    if match['s'] == 'S':
        if m == 0:
            raise ConversionError(f'Invalid data type. '
                                  f'Significand should be greater than zero in the given data type {data_type}.')
        s = True
        m -= 1
    else:
        s = False

    if m == 0 and e == 0:
        raise ConversionError(f'Invalid data type. '
                              f'The final data type {data_type} should not be of zero length.')

    # calculate maximum and minimum value
    min_val = - (1 << m) if s is True else 0
    max_val = (1 << m) - 1 / (1 << e)

    # check if the value feats in variable type
    if error_strategy == 'raise' and not (min_val <= float_value <= max_val):
        raise ConversionError(
            f'Invalid value. Given value {float_value} does not fit in given data type {data_type}. '
            f'Acceptable range: [{min_val}, {max_val}].')

    if error_strategy == 'skip':
        if float_value <= min_val:
            return 1 << (m + e) if s is True else 0
        if float_value >= max_val:
            return (1 << (m + e)) - 1

    # convert
    fixed_value = round(float_value * (1 << e))

    # fix negative value
    if float_value < 0 and fixed_value != 0:
        fixed_value = abs(fixed_value) | (1 << (m + e))  # convert to positive and add sign bit

    return fixed_value


def fixed_to_float(data_type: str, fixed_value: int) -> float:
    """
    Converts fixed into a float representation of a number.

    data_type should contain fixed number type representation.
    First char should be U (unsigned) or S(signed). Next is the number of bits for significand (integer part).
    Next should come the Q char and next is the number of bits for exponent (fractional part).
    Example: S4Q4. Here the number of significand bits is 3, 1 bit is taken by sign. And next 4 bits represent exponent.
    In total here is a 8 bits number.

    :param data_type: string containing data type of the fixed number
    :param fixed_value: int value to convert from to float
    """

    # check value
    if not isinstance(fixed_value, int):
        raise ConversionError(f'Invalid value type: {type(fixed_value)}.')

    # parse data_type
    match = _r.search(data_type)
    if not match:
        raise ConversionError(f'Invalid data type. '
                              f'Given data type {data_type} should meet the rules. See function description.')

    # get mantissa value, check it later
    m = int(match['m'])  # mantissa

    # get exponent value and check it
    e = int(match['e'])  # exponent

    # get sign value
    if match['s'] == 'S':
        if m == 0:
            raise ConversionError(f'Invalid data type. '
                                  f'Significand should be greater than zero in the given data type {data_type}.')
        s = 1
        m -= 1
    else:
        s = 0

    if m == 0 and e == 0:
        raise ConversionError(f'Invalid data type. '
                              f'The final data type {data_type} should not be of zero length.')

    if fixed_value < 0:
        raise ConversionError(f'Invalid value. The value {fixed_value} should be positive.')

    mask = (1 << (s + m + e)) - 1  # all bits
    if not (fixed_value | mask == mask):  # set all bits and check if the value does not exceed the masked data type
        raise ConversionError(f'Invalid value. '
                              f'The given value {fixed_value} does not fit in the given data type {data_type}.')

    # convert
    if fixed_value == 0:
        float_value = 0
    elif s:  # from signed value
        mask = (1 << (m + e))  # mask for sign bit
        lowest = fixed_value & mask  # value that contains only sign bit, also it is a lowest possible float value
        if lowest:  # if sign bit is set
            if lowest == fixed_value:  # if this is a lowest value
                float_value = - (1 << m)
            else:
                float_value = - (fixed_value & (mask - 1)) / (1 << e)
        else:  # has no sign
            float_value = fixed_value / (1 << e)
    else:  # from unsigned
        float_value = fixed_value / (1 << e)

    return float(float_value)


if __name__ == '__main__':
    import unittest

    class TestsFloatToFixed(unittest.TestCase):
        positive_tests = (
            # table with all possible values for S2Q2
            (('S2Q2', 0.00), 0),
            (('S2Q2', 0.25), 0b0001),
            (('S2Q2', 0.50), 0b0010),
            (('S2Q2', 0.75), 0b0011),
            (('S2Q2', 1.00), 0b0100),
            (('S2Q2', 1.25), 0b0101),
            (('S2Q2', 1.50), 0b0110),
            (('S2Q2', 1.75), 0b0111),
            (('S2Q2', -0.25), 0b1001),
            (('S2Q2', -0.50), 0b1010),
            (('S2Q2', -0.75), 0b1011),
            (('S2Q2', -1.00), 0b1100),
            (('S2Q2', -1.25), 0b1101),
            (('S2Q2', -1.50), 0b1110),
            (('S2Q2', -1.75), 0b1111),
            (('S2Q2', -2.00), 0b1000),

            # check round
            (('S2Q2', +0.20), 0b0001),  # 0.20 should be rounded to 0.25
            (('S2Q2', -0.20), 0b1001),  # -0.20 should be rounded to -0.25
            (('S2Q2', +0.10), 0),  # 0.10 should be rounded to 0
            (('S2Q2', -0.10), 0),  # -0.10 should be rounded to 0

            # check unsigned
            (('U2Q2', 0.0), 0),
            (('U2Q2', 3.75), 0b11_11),

            # check round for unsigned
            (('U2Q6', 4 - 1 / 2 ** 6), 0xFF),  # value below 4.0 should be rounded

            # now come the "skip" error strategy tests
            (('U2Q2', -0.01, 'skip'), 0),
            (('U2Q2', -0.25, 'skip'), 0),
            (('U2Q2', -0.50, 'skip'), 0),
            (('U2Q2', 4.01, 'skip'), 0b1111),
            (('U2Q2', 4.25, 'skip'), 0b1111),
            (('U2Q2', 4.5, 'skip'), 0b1111),
            (('S2Q2', -2.1, 'skip'), 0b1000),
            (('S2Q2', -2.25, 'skip'), 0b1000),
            (('S2Q2', -2.50, 'skip'), 0b1000),
            (('S2Q2', 1.76, 'skip'), 0b0111),
            (('S2Q2', 2.0, 'skip'), 0b0111),
            (('S2Q2', 2.25, 'skip'), 0b0111),

            # zero handling
            (('S1Q2', 0.00), 0),
            (('S1Q2', 0.25), 0b0_01),
            (('S1Q2', 0.50), 0b0_10),
            (('S1Q2', 0.75), 0b0_11),
            (('S1Q2', 1.00, 'skip'), 0b0_11),  # overflow
            (('S1Q2', -0.25), 0b1_01),
            (('S1Q2', -0.50), 0b1_10),
            (('S1Q2', -0.75), 0b1_11),
            (('S1Q2', -1.00), 0b1_00),
            (('S1Q2', -1.25, 'skip'), 0b1_00),  # underflow
            (('U0Q2', 0.00), 0),
            (('U0Q2', 0.25), 0b_01),
            (('U0Q2', 0.75), 0b_11),
            (('U0Q2', 1.00, 'skip'), 0b_11),  # overflow
            (('U0Q2', -0.1, 'skip'), 0b_00),  # underflow
            (('S2Q0', 0.), 0),
            (('S2Q0', 1.), 0b01),
            (('S2Q0', 2., 'skip'), 0b01),  # overflow
            (('S2Q0', -1.), 0b11),
            (('S2Q0', -2.), 0b10),
            (('S2Q0', -3., 'skip'), 0b10),  # underflow
            (('U2Q0', 0.), 0),
            (('U2Q0', 1.), 0b01),
            (('U2Q0', 2.), 0b10),
            (('U2Q0', 3.), 0b11),
            (('U2Q0', 4., 'skip'), 0b11),  # overflow
            (('U2Q0', -1., 'skip'), 0),  # underflow
        )

        def test_positive(self):
            for input_data, expected_output in self.positive_tests:
                with self.subTest(input_data=input_data, expected_output=expected_output):
                    output = float_to_fixed(*input_data)
                    self.assertEqual(output, expected_output)

        negative_tests = (
            # invalid data type
            (('U2Q', 0.0), 'Invalid data type'),
            (('S2Q', 0.0), 'Invalid data type'),
            (('UQ2', 0.0), 'Invalid data type'),
            (('SQ2', 0.0), 'Invalid data type'),
            (('U0Q0', 0.0), 'Invalid data type'),
            (('S0Q0', 0.0), 'Invalid data type'),
            (('S1Q0', 0.0), 'Invalid data type'),

            # invalid error strategy
            (('U2Q2', 0.0, 'pass'), 'Invalid error strategy'),

            # invalid type of passed value
            (('S2Q2', 1), 'Invalid value type'),

            # boundary values
            (('U0Q8', 4.0, 'raise'), 'Invalid value'),
            (('U2Q2', -0.01, 'raise'), 'Invalid value'),
            (('S2Q2', 1.76, 'raise'), 'Invalid value'),
            (('S2Q2', -2.01, 'raise'), 'Invalid value'),
        )

        def test_negative(self):
            for input_data, expected_output in self.negative_tests:
                with self.subTest(input_data=input_data, expected_output=expected_output):
                    with self.assertRaises(ConversionError) as e:
                        float_to_fixed(*input_data)
                    self.assertIn(expected_output, str(e.exception))

    class TestsFixedToFloat(unittest.TestCase):
        positive_tests = (
            # table for S2Q2
            (('S2Q2', 0b00_00), +0.00),
            (('S2Q2', 0b00_01), +0.25),
            (('S2Q2', 0b00_10), +0.50),
            (('S2Q2', 0b00_11), +0.75),
            (('S2Q2', 0b00_11), +0.75),
            (('S2Q2', 0b01_00), +1.00),
            (('S2Q2', 0b01_01), +1.25),
            (('S2Q2', 0b01_10), +1.50),
            (('S2Q2', 0b01_11), +1.75),
            (('S2Q2', 0b10_00), -2.00),
            (('S2Q2', 0b10_01), -0.25),
            (('S2Q2', 0b10_10), -0.50),
            (('S2Q2', 0b10_11), -0.75),
            (('S2Q2', 0b11_00), -1.00),
            (('S2Q2', 0b11_01), -1.25),
            (('S2Q2', 0b11_10), -1.50),
            (('S2Q2', 0b11_11), -1.75),

            # partial table for U2Q2
            (('U2Q2', 0b00_00), 0.00),
            (('U2Q2', 0b00_01), 0.25),
            (('U2Q2', 0b00_10), 0.50),
            (('U2Q2', 0b10_00), 2.00),
            (('U2Q2', 0b10_01), 2.25),
            (('U2Q2', 0b11_11), 3.75),

            # U4Q2 data type
            (('U4Q2', 0b0000_00), 0),
            (('U4Q2', 0b0001_00), 1),
            (('U4Q2', 0b0001_01), 1.25),
            (('U4Q2', 0b1000_01), 8.25),

            # S4Q2 data type
            (('S4Q2', 0b1000_01), -0.25),
            (('S4Q2', 0b1000_00), -8),
            (('S4Q2', 0b1111_11), -7.75),

            # S4Q4 data type
            (('S4Q4', 0b1000_0001), -0.0625),
            (('S4Q4', 0b1000_0000), -8),

            # zero values handling
            (('S2Q0', 0b00), 0.0),
            (('S2Q0', 0b01), 1.0),
            (('S2Q0', 0b11), -1.0),
            (('S2Q0', 0b10), -2.0),
            (('S1Q1', 0b00), 0),
            (('S1Q1', 0b01), 0.5),
            (('S1Q1', 0b11), -0.5),
            (('S1Q1', 0b10), -1),
            (('U0Q1', 0), 0),
            (('U0Q1', 1), 0.5),
            (('U1Q0', 0), 0),
            (('U1Q0', 1), 1),
        )

        def test_positive(self):
            for input_data, expected_output in self.positive_tests:
                with self.subTest(input_data=input_data, expected_output=expected_output):
                    output = fixed_to_float(*input_data)
                    self.assertEqual(output, expected_output)

        negative_tests = (
            # overflow
            (('S2Q2', 0b1_00_00), 'Invalid value'),
            (('U0Q4', 0b1_00_00), 'Invalid value'),

            # negative value
            (('S2Q2', -1), 'Invalid value'),

            # invalid data type
            (('U2Q', 0), 'Invalid data type'),
            (('S2Q', 0), 'Invalid data type'),
            (('UQ2', 0), 'Invalid data type'),
            (('SQ2', 0), 'Invalid data type'),
            (('U0Q0', 0), 'Invalid data type'),
            (('S0Q0', 0), 'Invalid data type'),
            (('S1Q0', 0), 'Invalid data type'),
        )

        def test_negative(self):
            for input_data, expected_output in self.negative_tests:
                with self.subTest(input_data=input_data, expected_output=expected_output):
                    with self.assertRaises(ConversionError) as e:
                        fixed_to_float(*input_data)
                    self.assertIn(expected_output, str(e.exception))

    unittest.main()
