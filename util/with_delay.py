from functools import wraps
from datetime import timedelta
from time import sleep


def with_delay(total_delay: timedelta,
               sleep_delay: timedelta,
               to_catch=(AssertionError, ),
               strict=True):
    """
    Description:
        Decorator for cycling execution of a function till it returns without throwing any error.
        It can be used for functions that should wait an input, variable change and so on.

        When original function is called, if it return a result, it is returned from a decorator.
        If in same call any assertion that is listed in to_catch is raised, original function will be called
          once again in sleep_delay.
        After total_delay if error from to_catch does not disappear, actual error will be risen.
        If original function throws error not listed in to_catch list, it will be propagated outside the decorator.

        :param total_delay: Total delay to perform repeated function call.
        :param sleep_delay: Sleep time between function calls.
        :param to_catch: Exceptions to ignore to continue cycling.
        :param strict: If True than can raise any function exception not listed in to_catch list.
                       If False, than all exception (based on Exception) will be suppressed.

    Usage:
        with_delay(timedelta(minutes=3), timedelta(seconds=30))
        def function():
            some_bool_arg = get_some_bool_arg()
            assert some_bool_arg is True

        In this case will be performed validation multiple times until some_bool_arg becomes True.
        Every 30 seconds and during 3 minutes function will be executed periodically until timeout.
        After timeout will try to execute function without catching an exception.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            end_time = datetime.today() + total_delay
            while datetime.today() < end_time:
                try:
                    return function(*args, **kwargs)
                except to_catch:  # catch only selected exceptions
                    sleep(sleep_delay.total_seconds())
                except Exception:  # catch remaining exceptions
                    if strict is True:
                        raise
                    else:
                        sleep(sleep_delay.total_seconds())
            # execute original function without try-except block
            # as total_delay was passed
            return function(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == '__main__':
    import unittest
    from datetime import datetime

    class TestCase(unittest.TestCase):
        # todo mock sleep function
        def test_timeout(self):
            """
            Expected sequence: f(), sleep(0.7), f(), sleep(0.7), f() raises AssertionError.
            """
            @with_delay(timedelta(seconds=1), timedelta(seconds=0.7))
            def f():
                raise AssertionError
            start = datetime.today()
            with self.assertRaises(AssertionError):
                f()
            end = datetime.today()
            delta = end - start
            # expected delta: 0.7[s] * 2 = 1.4[s]
            # tolerance: 0.1[s]
            self.assertTrue(timedelta(seconds=1.3) <= delta <= timedelta(seconds=1.5))

        def test_no_timeout(self):
            """
            Expected sequence: f(), sleep(0.7), f() returns None
            """
            c = 0
            @with_delay(timedelta(seconds=1), timedelta(seconds=0.7))
            def f():
                nonlocal c
                c += 1
                if c <= 1:  # first call raise AssertionError
                    raise AssertionError
                # return None
            start = datetime.today()
            f()
            end = datetime.today()
            delta = end - start
            # expected delta: 0.7[s]
            # tolerance: 0.1[s]
            self.assertTrue(timedelta(seconds=0.6) <= delta <= timedelta(seconds=0.8))

        def test_no_delay(self):
            """
            Expected sequence: f() returns None
            """
            @with_delay(timedelta(seconds=1), timedelta(seconds=0.7))
            def f():
                pass
            start = datetime.today()
            f()
            end = datetime.today()
            delta = end - start
            # expected delta: 0[s]
            # tolerance: 0.1[s]
            self.assertTrue(delta <= timedelta(seconds=0.1))

    unittest.main()
