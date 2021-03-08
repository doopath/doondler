""" Testing of the config handler file. """
import os
import sys

from modules.config import Config
from modules.paths import get_path
from tests.success import success
from tests.test_box import test_box

config = Config()

CONFIG_PATH = get_path("config")
LOGS_PATH = get_path("logs")


def warn_before_testing():
    """ Ask user if he wants to continue. """
    question = "Your config file will be removed while testing, "\
        "do you want to continue? (y/n): "
    answer = input(question).upper()

    if answer == "N":
        print("Testing was interrupted.")
        sys.exit()
    elif answer != "N" and answer != "Y":
        print("Please, answer y or n.")
        warn_before_testing()


def remove_file(path: str):
    """ Remove file if it exists. """
    if os.path.isfile(path):
        os.remove(path)


def is_valid_config_size(config_path: str):
    """ Check if config size is valid. """
    config = open(config_path)
    config_content = config.read()
    config.close()

    if sys.getsizeof(config_content) < 50:
        return False

    return True


def make_test():
    """ Testing of the make method. """
    print("\nTesting of the make method...")

    remove_file(CONFIG_PATH)
    remove_file(LOGS_PATH)

    os.system("python3 ../main.py --init")

    assert os.path.isfile(CONFIG_PATH), "Config file does not exists!"
    assert os.path.isfile(LOGS_PATH), "Log file does not exists! "\
        "is incorrect (less than 80 byte)!"

    success("Make method tests")


def remove_test():
    """ Testing of the remove method. """
    print("\nTesting of the remove method...")

    config.remove()

    assert not os.path.isfile(CONFIG_PATH), "Config exists after removing!"

    success("Remove method tests")


def remake_test():
    """ Testing of the remake method. """
    print("\nTesting of the remake method...")

    os.system("python3 ../main.py -reinit")

    assert os.path.isfile(CONFIG_PATH), "Config file does not exists!"
    assert os.path.isfile(LOGS_PATH), "Log file does not exists!"

    success("Remake method tests")


@test_box
def main():
    """ Tests facade. """
    warn_before_testing()

    remake_test()
    remove_test()
    make_test()

    success("Config tests")


if __name__ == "__main__":
    main()

