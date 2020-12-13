class MultiMethod:
    def __init__(self, name):
        self.name = name
        self.type_map = {}

    def __call__(self, *args):
        instance = args[0]
        args = args[1:]
        types = tuple(arg.__class__ for arg in args)
        function = self.type_map.get(types)
        if function is None:
            raise TypeError('no match')
        return function(instance, *args)

    def register(self, types, function):
        if types in self.type_map:
            raise TypeError('duplicate registration')
        self.type_map[types] = function


registry = {}


def multimethod(*types):
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod(name)
        mm.register(types, function)
        return mm

    return register


if __name__ == '__main__':
    from types import MethodType

    @multimethod(int)
    def f(self, x: int):
        print('int')

    @multimethod(float)
    def f(self, x: float):
        print('float')

    @multimethod(str)
    def f(self, x: str):
        print('str')

    class A:
        pass

    A.f = MethodType(f, A)
    # A.f = f  # cannot be used, todo figure out why
    print(A.f)
    print(f)

    a = A()
    a.f(1)
    a.f(2.0)
    a.f('3')
