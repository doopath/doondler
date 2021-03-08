""" A cache saver module. """


class Cacher:
    """
        A class of a cache saver.

    """
    _cache = {}

    def cache(self, func):
        """ Memoize and cache value. """
        def gen_cache(name: str, args: tuple, kwargs: dict):
            cache_key = name + '-'

            for arg in args:
                cache_key += str(arg) + "-"
            for key, value in kwargs.items():
                cache_key += key + "=" + str(value)

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
