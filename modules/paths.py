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
        "config-copy": "/.doondlerc.copy",
        "logs": "/.doondler_logs",
        "note": "/.note_"
    }


def get_absolute_path(name: str) -> str:
    """ Get absolute path. """
    if name[1:5] != "home":
        return f"{get_home_dir()}{name}"

    return name


def paths_decorator(func):
    """ Get dict of any paths. """

    def inner(name: str) -> str:
        local_path = func(name)
        absolute_path = get_absolute_path(local_path)

        if absolute_path == local_path * 2:
            return local_path

        return absolute_path

    return inner


@paths_decorator
def get_path(name: str):
    """ Get path by name. """
    return get_paths()[name]

