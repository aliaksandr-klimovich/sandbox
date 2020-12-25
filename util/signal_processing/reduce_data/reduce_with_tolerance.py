from typing import Union
from collections.abc import Iterator, Generator


def reduce_with_tolerance(
        data: Iterator[float, int],
        tolerance: Union[float, int],
        strategy: str = 'mean') -> \
            Generator[tuple[tuple[float, int], float]]:
    """
    Returns reduced list of values, grouped by equal with tolerance sibling values.
    Yields tuple of reduced values.

    :param data: Data set.
    :param tolerance: Absolute tolerance to apply.
    :param strategy: How to apply tolerance value.
        'mean' - Mean of each reduced set of data is calculated and compared with current value.
                 Reduced set of data is always a "previous" set of contantly inreasing data
                 till new reduced data comes in (when tolerance is exceeded).
        'previous' - Previous value is compared with the current.

    Examples:
    >>> list(reduce_with_tolerance([1.1, 0.9, 2.], 0.5))
    [(1.1, 0.9), (2.0,)]
    """

    iter_data = iter(data)

    try:
        values = [next(iter_data)]
    except StopIteration:
        return

    if strategy == 'mean':

        f_sum = values[0]
        n = 1

        for current_value in iter_data:
            values_mean = f_sum / n
            if values_mean - tolerance <= current_value <= values_mean + tolerance:
                values.append(current_value)
                f_sum += current_value
                n += 1
            else:
                yield tuple(values)
                values = [current_value]
                f_sum = current_value
                n = 1

        # values_mean = f_sum / n
        yield tuple(values)

    elif strategy == 'previous':

        previous_value = values[0]

        for current_value in iter_data:
            if previous_value - tolerance <= current_value <= previous_value + tolerance:
                values.append(current_value)
            else:
                yield tuple(values)
                values = [current_value]
            previous_value = current_value

        yield tuple(values)
