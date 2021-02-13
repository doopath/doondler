""" A module that contains any errors using in sea_battle module. """


class HitError(Exception):
    """
        Error of hitting.
        It is occurring if you hit a field that was already blown up.
        After this error the program do not must to abort, user should lose one try.
    """


class FillingError(Exception):
    """
        Error of filling the playground.
        It is occurring when you set incorrect coordinates for a ship.
        After this error the program should be aborted.
    """
