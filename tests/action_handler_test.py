""" Testing of the action handler module. """
import time

from tests.success import success
from tests.test_box import test_box
from tests.test_mock import *
from modules.action_handler import *


mock_system_args = ["action_handler_test.py", "-test1", "Michael", "--test2"]


def reduce_test():
    """ Testing of the reduce method. """
    action_handler = ActionHandler(mock_system_args)
    action_handler.reduce()

    assert mocks["name"] != "", "Action handler did not change the mock name value!"
    assert mocks["time"] != 0, "Action handler did not change the mock time value!"


@test_box
def main():
    """ Main function of the action handler tests. """
    reduce_test()

    success("Action handler tests")


if __name__ == "__main__":
    main()
