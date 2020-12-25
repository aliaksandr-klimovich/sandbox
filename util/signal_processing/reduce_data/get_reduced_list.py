from collections.abc import Iterator


# it is better to use list(reduce())
def get_reduced_list(data: Iterator) -> list:
    """
    Returns reduced list of values. Sibling values are grouped by value.

    Example:
    >>> list(get_reduced_list([1, 2, 2, 3, 3, 3, 1]))
    [1, 2, 3, 1]
    """
    result = []
    iter_data = iter(data)
    try:
        previous_value = next(iter_data)
    except StopIteration:
        return result
    result.append(previous_value)
    for current_value in iter_data:
        if current_value != previous_value:
            result.append(current_value)
            previous_value = current_value
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
