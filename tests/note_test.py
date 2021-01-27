""" Testing of the note module. """
from time import time
from time import sleep
import os
import sys

from modules.note import Note
from modules.paths import get_path
from tests.success import success
from tests.test_box import test_box


TIMEOUT = 3 # Seconds
DEADLINE = round(time()) + TIMEOUT
NOTE_PATH = get_path("note") + str(DEADLINE)
LOG_PATH = get_path("note") + f"{DEADLINE}_output"

TIMEOUT_2 = 7
DEADLINE_2 = round(time()) + TIMEOUT_2
NOTE_PATH_2 = get_path("note") + str(DEADLINE_2)
LOG_PATH_2 = get_path("note") + f"{DEADLINE_2}_output"


def check_if_file_exists(path: str):
    """ Check if created note exists. """
    exists = os.path.isfile(path)

    if exists:
        success(f"Test of the {path} file existing.")

    return os.path.isfile(path)



def check_note_size():
    """ Check if created note is correct and has right size. """
    note = open(NOTE_PATH)
    note_content = note.read()

    assert sys.getsizeof(note_content) > 500, "Note has incorrect size!"

    success("Test of note size")


def wait_note_deleting():
    """ Wait until a note is don't have to execute. """
    while round(time()) < DEADLINE + 2:
        sleep(1)


def create_test():
    """ Testing of the create method. """
    note = Note("Doopath", "Test message", full_deadline=DEADLINE)
    note.create()
    sleep(1)

    assert check_if_file_exists(NOTE_PATH), "Note doesn't exists after creating!"
    assert check_if_file_exists(LOG_PATH), "Log file doesn't exists after creating!"

    check_note_size()
    wait_note_deleting()

    assert not check_if_file_exists(NOTE_PATH), "Note existing after ended deadline!"
    assert not check_if_file_exists(LOG_PATH), "Log file existing after ended deadline!"

    success("Test of the note's create method")


def delete_test():
    """ Testing of the delete method. """
    note2 = Note("Doopath", "Test message", full_deadline=DEADLINE_2)
    note2.create()
    note2.delete()

    assert not check_if_file_exists(NOTE_PATH_2), "Note existing after deleting!"
    assert not check_if_file_exists(LOG_PATH_2), "Log file existing after deleting!"

    success("Test of the note's delete method")


@test_box
def main():
    """ All your tests here. """
    create_test()
    delete_test()

    sleep(1)
    success("Note module test")


if __name__ == "__main__":
    main()

