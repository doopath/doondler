""" Notify dev that testing was successful. """
from modules.colors import to_green


def success(test_name: str):
    """ Show message about successfully completed tests. """
    print(to_green(f"{test_name} successfully completed!"))
