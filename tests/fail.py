""" Fail function module. """
import sys
import traceback

from modules.colors import to_yellow
from modules.colors import to_red
from modules.colors import lred
from modules.colors import no_color


def fail(error):
    """ Show error message and exit. """
    # ANSI colors
    print(to_yellow(str(error)))
    print(to_red("Test was failed!"))

    print(lred)  # Make traceback red.
    traceback.print_exc()
    print(no_color)

    sys.exit()
