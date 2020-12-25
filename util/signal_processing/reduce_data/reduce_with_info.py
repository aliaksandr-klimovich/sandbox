from collections.abc import Iterator, Generator


def reduce_with_info(data: Iterator) -> Generator[tuple]:
    """
    Returns reduced data in `ReducedDataInfo` object (which contains information about reduced data).
    Info objects consists of:
    - index of first reduced element;
    - value of first reduced element;
    - reduced elements count.

    Example: 
    >>> list(reduce_with_info([1, 2, 2, 3, 3, 3, 1]))
    [(0, 1, 1), (1, 2, 2), (3, 3, 3), (6, 1, 1)]

    Note, implementation uses "next" value provision, i.e. yields info of the already reduced data while
    new value from data is preserved for future yield.
    """

    # Create iterator over the data
    iter_data = iter(data)

    # Get first value, store it. Also check for empty data.
    try:
        previous_value = next(iter_data)
    except StopIteration:
        return

    # Initialize variables for `for` cycle and for last reduced data info if any.
    start_index = 0
    current_index = 1

    # Iterate over the rest of the data
    for current_value in iter_data:
        if current_value != previous_value:
            length = current_index - start_index
            yield start_index, previous_value, length
            start_index = current_index
            previous_value = current_value
        current_index += 1

    length = current_index - start_index
    yield start_index, previous_value, length
