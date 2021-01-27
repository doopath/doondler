""" ANSI colors module. """

prefix = "\033["

black = f"{prefix}0;30m"
dgray = f"{prefix}1;30m"
red = f"{prefix}0;31m"
lred = f"{prefix}1;31m"
green = f"{prefix}0;32m"
lgreen = f"{prefix}1;32m"
brown = f"{prefix}0;33m"
yellow = f"{prefix}1;33m"
blue = f"{prefix}0;34m"
lblue = f"{prefix}1;34m"
purple = f"{prefix}0;35m"
lpurple = f"{prefix}1;35m"
cyan = f"{prefix}0;36m"
lcyan = f"{prefix}1;36m"
lGray = f"{prefix}0;37m"
white = f"{prefix}1;37m"
no_color = f"{prefix}0m"


def to_green(string: str):
    """ Make a green string from initial string. """
    return f"{lgreen}{string}{no_color}"


def to_red(string: str):
    """ Make a green string from initial string. """
    return f"{lred}{string}{no_color}"


def to_yellow(string: str):
    """ Make a green string from initial string. """
    return f"{yellow}{string}{no_color}"
