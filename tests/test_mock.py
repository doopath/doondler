""" Mock test module. """

mocks = {
    "time": 0,
    "name": ""
}


def test1_mock(name: str):
    """ Mock function to redefine name. """
    mocks["name"] = name


def test2_mock():
    """ Mock function to redefine time. """
    mocks["time"] = 1
