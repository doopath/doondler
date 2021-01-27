""" A cache saver module. """


class Cacher:
    """ A class of cache saver. """
    _cache = {}

    def cache(self, func: callable):
        """ Memoize and cache value. """
        def gen_cache(name: str, args: tuple, kwargs: dict):
            cache_key = name + '-'

            for arg in args:
                cache_key += str(arg) + "-"
            for _, kwarg in kwargs.items():
                cache_key += _ + "=" + str(kwarg)

            return cache_key[:-1]

        def inner_wrapper(*args, **kwargs):
            cache_key = gen_cache(func.__name__, args, kwargs)

            if cache_key in Cacher._cache:
                return self._cache[cache_key]
            else:
                self._cache[cache_key] = func(*args, **kwargs)

                return self._cache[cache_key]

        return inner_wrapper


cacher = Cacher()


@cacher.cache
def fib(num: int):
    """ Measure a fibanacci number."""
    my_fib = [0, 1]

    for i in range(num - 1):
        my_fib = [my_fib[1], my_fib[0] + my_fib[1]]

    return my_fib[1]
