print('Meta definition')


class Meta(type):
    def __new__(mcs, name, bases, namespace):
        print('Meta __new__:', mcs, name, namespace)
        ret = type.__new__(mcs, name, bases, namespace)  # class creation
        print('Meta __new__ ret:', ret)
        return ret

    def __init__(cls, name, bases=None, namespace=None):
        print('Meta __init__:', cls, name, bases, namespace)
        super(Meta, cls).__init__(name, bases, namespace)  # can be suppressed in some cases
        print('Meta post __init__:', cls, name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        print('Meta __call__:', cls, args, kwargs)
        ret = type.__call__(cls, *args)  # class instance creation
        print('Meta __call__ ret:', ret)
        print('Meta __call__ ret __dict__:', ret.__dict__)
        return ret


print('\nBase definition')


class Base(metaclass=Meta):
    def __new__(cls, *args, **kwargs):
        print('Base __new__:', cls, args, kwargs)
        ret = super(Base, cls).__new__(cls)
        print('Base __new__ ret:', ret)
        return ret

    def __init__(self, *args, **kwargs):
        print('Base __init__:', self, args, kwargs)

    def __call__(self, *args, **kwargs):
        print('Base __call__:', self, args, kwargs)


print('\nB definition')


class B(Base):
    prop = True

    def func(self):
        pass

    def __init__(self, p=2, *args):
        super(B, self).__init__(*args, p=2)
        self.p = p


print('\nCreate B instance')
b = B(1, p=2)


print('\nCall B instance')
b(3, b=4)


print('\nCreate Base2 class')
Base2 = Meta('Base2', (), {})

print('\nCreate B2 class')
B2 = type('B2', (Base2,), {})  # Meta will be used to create B2 class

print('\nCreate B2 instance')
b2 = B2()

print('\nTest B2 class')
def B2_call(self, *args, **kwargs):
    print(self, args, kwargs)
B2.__call__ = B2_call
b2(1, a=2)
