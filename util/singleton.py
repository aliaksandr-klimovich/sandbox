
# Most preferable way to create singletons is to use a metaclass.

class SingletonMeta(type):
    def __init__(cls, name, bases=None, attr=None):
        super().__init__(name, bases, attr)
        # create instance holder after class is created
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        # instance creation requested
        # check instance holder; if have no instance, then create one
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Singleton(metaclass=SingletonMeta):
    """
    Implementation of the singleton class.
    This class is supposed to have only one instance.
    """


# Other shit goes out of module import
if __name__ == '__main__':

    import unittest

    class TestSingleton(unittest.TestCase):
        def test(self):
            class A(Singleton): pass
            class B(Singleton): pass
            class C(A): pass
            a = A()
            a2 = A()
            b = B()
            b2 = B()
            c = C()
            c2 = C()

            # check that the instance is of the proper class
            self.assertIsInstance(a, A)
            self.assertIsInstance(a2, A)
            self.assertIsInstance(b, B)
            self.assertIsInstance(b2, B)
            self.assertIsInstance(c, C)
            self.assertIsInstance(c2, C)

            # check that second attempt to create an instance results in the same instance
            self.assertIs(a, a2)
            self.assertIs(b, b2)
            self.assertIs(c, c2)

            # check that other class instances are created
            self.assertIsNot(a, b)
            self.assertIsNot(a, b2)
            self.assertIsNot(a, c)
            self.assertIsNot(a, c2)
            self.assertIsNot(b, c)
            self.assertIsNot(b, c2)

    # Another approach to make a singleton is
    # to create a metaclass that converts all methods to class methods by default.
    class SingletonMeta2(type):
        def __new__(mcs, name, bases, namespace):
            cls = type.__new__(mcs, name, bases, namespace)
            # after class is created, decorate each method
            for k, v in cls.__dict__.items():
                if callable(v) and not hasattr(v, '__self__'):
                    setattr(cls, k, classmethod(v))
            return cls

        def __call__(cls, *args, **kwargs):
            raise RuntimeError('Cannot create class instance of the singleton.')

    class Singleton2(metaclass=SingletonMeta2):
        """
        Implementation of the singleton class.
        You cannot create class instance.
        All methods are decorated with `classmethod` by its metaclass.
        """

    class TestSingleton2(unittest.TestCase):
        def test(self):
            class A(Singleton2):
                def f_a(cls, x):
                    return cls, x
            class B(A):
                def f_b(cls, x):
                    return cls, x

            # check that cannot create instance of the class
            with self.assertRaises(RuntimeError):
                A()
            with self.assertRaises(RuntimeError):
                B()

            # check that class method is called with a class, not the instance
            cls, x = A.f_a(1)
            self.assertIs(cls, A)
            self.assertEqual(x, 1)
            cls, x = B.f_b(1)
            self.assertIs(cls, B)
            self.assertEqual(x, 1)

    # Just an example, if you trust your team ;)
    class SampleSingletonClass:
        @classmethod  # every method should be decorated with `classmethod`
        def f(cls, x):
            return x

    # Next approach is to use __new__ method of the class
    # Not the best approach as all class instances are located in one place, the `_instances` dictionary.
    class Singleton3:
        """
        Implementation of the singleton class.
        No metaclass is used here.
        """
        _instances = {}

        def __new__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super().__new__(cls, *args, **kwargs)
            return cls._instances[cls]

    class TestSingleton3(unittest.TestCase):
        def test(self):
            class A(Singleton3): pass
            a = A()
            self.assertIsInstance(a, A)

            a2 = A()
            self.assertIsInstance(a2, A)
            self.assertIs(a, a2)

            class B(A): pass
            b = B()
            self.assertIsInstance(b, B)
            self.assertIsNot(a, b)

            b2 = B()
            self.assertIsInstance(b2, B)
            self.assertIs(b, b2)

    # Class decorator approach
    def singleton(cls):
        """
        Class decorator.
        Actually returns a function. This is important, as you cannot access class methods.
        """
        instances = {}

        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

        return get_instance

    # Sorry, no tests here...

    # Using `get_instance` method. Java developers will appreciate this solution. :D
    # Right like Singleton3 (__new__ method is also a class method).
    class Singleton4:
        _instances = {}

        # prohibit to create instances with a call
        # def __init__(self):
        #     raise RuntimeError('Cannot create an instance of a singleton class. Use `get_instance` method instead.')

        # use only method that can create an instance
        @classmethod
        def get_instance(cls):
            if cls not in cls._instances:
                cls._instances[cls] = cls()  # wow! no args nor kwargs are passed to __init__!
            return cls._instances[cls]

    class TestSingleton4(unittest.TestCase):
        def test(self):
            class A(Singleton4): pass
            class B(Singleton4): pass
            class C(A): pass

            # with self.assertRaises(RuntimeError):
            #     A()
            # with self.assertRaises(RuntimeError):
            #     C()

            a = A.get_instance()
            a2 = A.get_instance()
            b = B.get_instance()
            c = C.get_instance()
            c2 = C.get_instance()

            self.assertIsInstance(a, A)
            self.assertIsInstance(a2, A)
            self.assertIsInstance(b, B)
            self.assertIsInstance(c, C)
            self.assertIsInstance(c2, C)

            self.assertIs(a, a2)
            self.assertIs(c, c2)


    # Finally, test it!
    unittest.main()
