""" Any paths of configs, log files et cetera. """
from os import path


def get_home_dir():
    """ Get user's home directory. """
    return path.expanduser("~")


def get_paths():
    """ Get any paths. """
    return {
        "home": get_home_dir(),
        "config": "/.doondlerc",
        "logs": "/.doondler_logs",
        "note": "/.note_"
    }


def get_absolute_path(name: str):
    """ Get absolute path. """
    if name[1:5] != "home":
        return f"{get_home_dir()}{name}"

    return name


def paths_decorator(func: callable):
    """ Get dict of any paths. """

    def inner(name: str):
        return get_absolute_path(func(name))

    return inner


@paths_decorator
def get_path(name: str):
    """ Get path by name. """
    return get_paths()[name]
