#! /usr/bin/env python3.9
""" Main module that runs all tests """

from modules.timeit import timeit
from tests.success import success
from tests import config_test
from tests import action_handler_test
from tests import config_writer_test
from tests import config_reader_test
from tests import note_test
from tests import yuigahama_test
from tests import config_prototype_test


# Put main functions of  your tests here.
def get_all_tests():
    """ Get a dict with all tests. """
    return {
        "Note": note_test.main,
        "Config": config_test.main,
        "ActionHandler": action_handler_test.main,
        "ConfigWriter": config_writer_test.main,
        "ConfigReader": config_reader_test.main,
        "YuigahamaHandler": yuigahama_test.main,
        "ConfigPrototype": config_prototype_test.main,
    }


def show_start_notify(test_name: str):
    """ Show a message about start of a test. """
    print(f"Start testing {test_name}...")


@timeit
def run_test(test: callable, test_name: str):
    """ Run one test. """
    show_start_notify(test_name)
    test()


@timeit
def main():
    """ All your tests here. """
    print("Start testing...\n")

    tests = get_all_tests()
    tests_count = len(tests)

    for test_name, test in tests.items():
        run_test(test, test_name)

    success(f"Any tests ({tests_count} / {tests_count})")


if __name__ == "__main__":
    main()
