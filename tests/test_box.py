""" Test module. """
from tests.fail import fail


def test_box(func: callable):
    """ Testing of some method or function. """
    def inner_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as error:
            fail(error)

    return inner_wrapper

