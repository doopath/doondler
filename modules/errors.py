""" Custom errors. """


class Warning(Exception):
    """ A warning. Occurring when the program behaves non-standard. """
    pass

class InitializationError(Exception):
    """ An error that occurring while initialization. """
    pass


class CalculationError(Exception):
    """ An error that occurring while calculation. """
    pass
