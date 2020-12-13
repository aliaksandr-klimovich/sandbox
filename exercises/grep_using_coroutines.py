import functools


def coroutine(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator
    return wrapper


@coroutine
def grep(pattern):
    print("Looking for %s" % pattern)
    while True:
        line = (yield pattern)
        if pattern in line:
            print(line)


g = grep("python")
g.send("bla-bla-bla")
g.send("PYTHON!!")
g.send("P-Y-T-H-O-N!!!")
g.send("oh.. just python...")


def countdown(n):
    print("Counting down from", n)
    while n >= 0:
        newvalue = (yield n)
        # If a new value got sent in, reset n with it
        if newvalue is not None:
            n = newvalue
        else:
            n -= 1


c = countdown(5)
for n in c:
    print(n)
    if n == 5:
        c.send(3)


def generator(first, last):
    for i in range(first, last):
        yield i


g = generator(1, 5)
for i in g:
    print(i)
