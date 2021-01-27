"""
    Testing of the yuigahama module.
    These tests thought Note module is valid.
"""
import os
from time import time
from time import sleep

from modules.yuigahama import Handler
from modules.user import User
from modules.paths import get_path
from tests.test_box import test_box
from tests.success import success


user = User()
user.create()
handler = Handler(user)
DEADLINE = round(time()) + 3
NOTE_PATH = get_path("note") + str(DEADLINE)


def check_if_file_exists(path: str):
    """ Check if file exists. """
    existence = os.path.isfile(path)
    test_name = f"Test of file {path}"

    assert existence, test_name
    success(test_name)


def wait_note_deleting(deadline: int):
    """ Wait while note is alive. """
    while time() * 1000 < deadline:
        sleep(1)


def make_note_test():
    """ Testing of the make_note method. """
    handler.make_note("Test", deadline=DEADLINE)
    check_if_file_exists(NOTE_PATH)

    success("Test of the yuigahama's make_note method")


@test_box
def main():
    """ Run all tests of yuigahama module. """
    make_note_test()

    success("Test of the yuigahama module")

if __name__ == "__main__":
    main()

