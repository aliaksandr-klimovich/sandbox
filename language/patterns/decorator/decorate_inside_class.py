"""
Warning! This is not a working code!!
"""

from functools import wraps


class DataObject(object):
    def cached(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            print('all cache:', self._cache)
            if f.__name__ not in self._cache:
                result = f(self, *args, **kwargs)
                self._cache[f.__name__] = []
                self._cache[f.__name__].append({'args': args,
                                                'kwargs': kwargs,
                                                'result': result})
                print('cache not found, saving as:', {'args': args,
                                                      'kwargs': kwargs,
                                                      'result': result})
            else:
                for c in self._cache[f.__name__]:
                    if c['args'] == args and c['kwargs'] == kwargs:
                        print('cache found:', c)
                        return c['result']
                result = f(self, *args, **kwargs)
                self._cache[f.__name__] = []
                self._cache[f.__name__].append({'args': args,
                                                'kwargs': kwargs,
                                                'result': result})
                print('cache not found, saving as:', {'args': args,
                                                      'kwargs': kwargs,
                                                      'result': result})
            return result

        return wrapper

    def _clear_cache(self):
        self._cache = {}

    def __init__(self):
        self._cache = {}

    @cached
    def method(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    data = DataObject()
    data.method()
    data.method()
    data.method(0, a=1)  # cache is replaced for some reason, todo fix cache
    data.method(0, a=1)
    data.method()
