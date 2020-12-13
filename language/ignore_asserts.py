#! /usr/bin/env python3 -O
# `O` means optimized

def f(x):
    assert isinstance(x, str)
    print(x)


if __name__ == '__main__':
    f('5')
    f(5)  # if run without parameters, AssertionError will be raised
