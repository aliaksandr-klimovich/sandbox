from functools import wraps


class A:
    def __init__(self, decorators=()):
        for d in decorators[::-1]:
            self.method = d(self.method)

    @staticmethod
    def method():
        print("Method")


def decorator_1(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("Decorator 1")
        return function(*args, **kwargs)
    return wrapper


def decorator_2(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("Decorator 2")
        return function(*args, **kwargs)
    return wrapper


a = A((decorator_1, decorator_2))
a.method()
