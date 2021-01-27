"""
    Config reader module tests.
    These tests require correct working of the config_writer module.
"""

import os
import sys
from modules.config_reader import ConfigReader
from modules.config_writer import ConfigWriter
from modules.paths import get_path
from tests.test_box import test_box
from tests.success import success


CONFIG_PATH = get_path("config")
config_reader = ConfigReader(CONFIG_PATH)


def check_config_size(config_content: str):
    """ Check if config size is correct. """
    config_size = sys.getsizeof(config_content)
    assert config_size > 50, "Incorrect config size (less than 50 bytes)"

    success("Config size test")


def check_config_length(config_content: str):
    """ Check config length is correct. """
    assert len(config_content) >= 4, "Incorrect config length!"

    success("Config length test")


def check_config_is_correct(config_content: str):
    """ Check if config has correct size (more than 50b) and length (more than 4 lines). """
    check_config_size(config_content)
    check_config_length(config_content)

    success("Config validation test")


def write_mock_parameter(name, value):
    """ Write mock name: value to the config. """
    config_writer = ConfigWriter(CONFIG_PATH)
    config_writer.write(name, value)


def check_if_correct_parameter(config_content: dict, name: str, value: str):
    """ Check if config has name: value attribute and it's correct. """
    assert config_content[name] == value, f"Wrong parameter in config after writing! "\
        f"{name}: {config_content[name]} instead of {name}: {value}."

    success("Read method successfully found written parameter.")


def erase_mock_parameter(name: str):
    """ Erase mock parameter from the config. """
    config_writer = ConfigWriter(CONFIG_PATH)
    config_writer.erase(name)


def check_if_parameter_not_exists(config_content: dict, name: str):
    """ Check if config hasn't some parameter. """
    parameter_existing = False

    for attribute in config_content:
        if attribute == name:
            parameter_existing = True

    assert parameter_existing is False, "Read method found erased parameter in the config."


def read_test():
    """ Test of the read method. """
    config_content = config_reader.read()
    check_config_is_correct(config_content)

    test_name = "mock_name"
    test_value = "mock_value"
    write_mock_parameter(test_name, test_value)

    config_content = config_reader.read()
    check_if_correct_parameter(config_content, test_name, test_value)

    erase_mock_parameter(test_name)
    config_content = config_reader.read()
    check_if_parameter_not_exists(config_content, test_name)

    check_config_is_correct(config_content)

    success("Test of the read method")


@test_box
def main():
    """ All tests of methods here. """
    read_test()

    success("Config reader test")


if __name__ == "__main__":
    main()

