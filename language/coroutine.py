def coroutine(f):
    """
    Decorator to use to start coroutine function without extra steps.
    """
    def start(*args, **kwargs):
        cr = f(*args, **kwargs)
        cr.next()
        return cr
    return start


# Example of coroutine
def countdown(n):
    print('Counting down from', n)
    while n >= 0:  # define exit condition
        new_value = (yield n)  # next() returns n, send(i) sets new_value to i (n is not set)
        # If a new value got sent in, reset `n` with it
        if new_value is not None:
            n = new_value
        else:
            n -= 1


c = countdown(5)
# there is no print here, `countdown(5)` only initializes generator
for n in c:  # next() called and print() is made inside countdown() function
    print(n)  # next() return value is printed
    if n == 5:  # condition to change generator behavior
        c.send(3)  # change generator behavior


print('-'*80)


# Example to show possible issue with several yields
def f(x):
    print('run')
    while True:
        new_x = yield x ** 2
        print(f'new_x: {new_x}')
        if new_x is None:
            # next() called
            pass
        else:
            # send() called
            x = new_x
            yield x


print('init')
f = f(1)
print('inited')
print(next(f))  # 1
print('-')
print(f.send(2))  # 2
print('-')
print(f.send(3))  # 4
# send(3) was called when previous execution ended with (yield x)
# so, execution continued till next yield, where x was 2
# 3 was ignored by (yield x)
print('-')
# as 3 was ignored, x contains 2
print(next(f))  # 4

# Finally, it seems like next() calls send(None)
