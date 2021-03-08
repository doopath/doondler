""" Executing time checker. """
from time import time


def timeit(func):
    """ Print executing time spent. """

    def inner_wrapper(*args, **kwargs):
        start = time() * 1000
        result = func(*args, **kwargs)
        print(f"Ended after {round(time() * 1000 - start)} ms.\n")

        return result

    return inner_wrapper
