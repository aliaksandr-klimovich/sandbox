from functools import wraps


def decorator_name(*dec_args, **dec_kwargs):

    # prepare usual decorator
    def decorate(function):
        @wraps(function)
        def wrapper(*func_args, **func_kwargs):

            # do something...
            print(dec_args, dec_kwargs)  # arguments of the decorator
            print(func_args, func_kwargs)  # arguments of the function

            return function(*func_args, **func_kwargs)
        return wrapper

    function = dec_args[0] if dec_args else None

    if callable(function):
        dec_args = dec_args[1:]

        # decorator was used like `@decorator_name`
        # do something...

        return decorate(function)

    else:

        # decorator was used like `@decorator_name(*args, **kwargs)`
        # do something...

        def decorator_with_args_and_kwargs(function):
            return decorate(function)

        return decorator_with_args_and_kwargs


# --- USAGE ------------------------------------------------------------------------------------------------------------

print('Decorating with @decorator_name')
@decorator_name
def f(*args, **kwargs): pass
f(3, b=4)

print('-'*80)

print('Decorating with @decorator_name()')
@decorator_name()
def f(*args, **kwargs): pass
f(3, b=4)

print('-'*80)

print('Decorating with @decorator_name(1, a=2)')
@decorator_name(1, a=2)
def f(*args, **kwargs): pass
f(3, b=4)

print('-'*80)

print('Decorating with @decorator_name(f1) where f1 = lambda: None')
print('Warning! This will not work as expected.')
f1 = lambda f: f
@decorator_name(f1, 1, a=2)  # f1 decorated instead of f2!
def f2(*args, **kwargs): pass
f2(3, b=4)

print('-'*80)

# to solve prior issue can pass f1 as a keyword
print('Decorating with @decorator_name(function=f1)')
def f1(): pass
@decorator_name(function=f1)
def f2(*args, **kwargs): pass
f2(1, a=2)

print('-'*80)

print('Check argument pass. Immutable.')
a = 0
@decorator_name(a)
def f(): pass
f()
a = 1
f()  # decorator argument did not change

print('-'*80)

print('Check argument pass. Mutable.')
a = [0]
@decorator_name(a)
def f(): pass
f()
a[0] = 1
f()  # list `a` is passed by link, so will be changed
