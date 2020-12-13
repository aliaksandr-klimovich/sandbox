import statistics
from collections import defaultdict
from functools import wraps
from timeit import default_timer as timer

from bidict1 import bidict as BiDict1
from bidict2 import bidict as BiDict2
from bidict3 import BiDict as BiDict3

stat = defaultdict(dict)


def print_stat():
    keys = ('max', 'min', 'mean')
    for f in stat:
        print(f'{f}:', end='')
        for key in keys:
            print(f' {key}={stat[f][key]:.3f}', end='')
        print()


def check_time(f):
    def get_stat(t: list):
        return {
            'max': max(t),
            'min': min(t),
            'mean': statistics.mean(t),
            #'pstdev': statistics.pstdev(t),
        }

    @wraps(f)
    def wrapper(*args, **kwargs):
        timings = []
        for _ in range(10):
            start = timer()
            for _ in range(1000):
                f(*args, **kwargs)
            end = timer()
            t = end - start
            timings.append(t)
        stat[f.__name__]['timings'] = timings
        stat[f.__name__].update(get_stat(timings))

    return wrapper


@check_time
def test_bidict1_set_value():
    bd = BiDict1()
    for i in range(100):
        bd[i] = i


@check_time
def test_bidict1_override_value():
    bd = BiDict1()
    for i in range(10):
        bd[i] = i + 1
    for i in range(10):
        bd[i] = i
    for i in range(10):
        bd[i] = i + 1
    for i in range(10):
        bd[i] = i


@check_time
def test_bidict2_set_value():
    bd = BiDict2()
    for i in range(100):
        bd[i] = i


@check_time
def test_bidict2_override_value():
    bd = BiDict2()
    for i in range(10):
        bd[i] = i + 1
    for i in range(10):
        bd[i] = i
    for i in range(10):
        bd[i] = i + 1
    for i in range(10):
        bd[i] = i


@check_time
def test_bidict3_set_value():
    bd = BiDict3()
    for i in range(100):
        bd[i] = i


@check_time
def test_bidict3_override_value():
    bd = BiDict3()
    for i in range(10):
        bd[i] = i + 1
    for i in range(10):
        bd[i] = i
    for i in range(10):
        bd[i] = i + 1
    for i in range(10):
        bd[i] = i


if __name__ == '__main__':
    d = globals().copy()
    for name, obj in d.items():
        if callable(obj) and name.startswith('test_'):
            obj()
    print_stat()
