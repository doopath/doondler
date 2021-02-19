""" A module that contains any errors using in sea_battle module. """


class HitError(Exception):
    """
        Error of hitting.
        It occurs if you hit a field that was already blown up.
        After this error the program do not must to abort, user should lose one try.
    """


class FillingError(Exception):
    """
        Error of filling the playground.
        It occurs when you set incorrect coordinates for a ship.
        After this error the program should be aborted.
    """


class PlaygroundValidationError(Exception):
    """
        Error of validating the playground.
        It occurs if a ship has incorrect fields list, for example when it located at A1 B1 A2 fields.
        After this error the program should say ship's fields list is incorrect.
    """
