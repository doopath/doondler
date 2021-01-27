""" Config writer module tests. """
from modules.config_writer import ConfigWriter
from modules.paths import get_path
from tests.success import success
from tests.test_box import test_box


CONFIG_PATH = get_path("config")
config_writer = ConfigWriter(CONFIG_PATH)


def get_config_lines(config_content: str):
    """ Get any lines in configuration file. """
    return config_content.split("\n")[:-1]


def get_guess_content(name: str, value: str):
    """ Get guess config content. """
    return {"name": name, "value": value}


def get_config_content():
    """ Get content (as string) of the configuration file. """
    with open(CONFIG_PATH) as config:
        config_content = config.read()

    return config_content


def get_test_content(config_line: str):
    """ Get test config content from config line. """
    items = config_line.split("=")
    items[0] = items[0].strip()
    items[1] = items[1].strip()

    return {"name": items[0], "value": items[1]}


def compare_config_content(guess: dict, real: dict, position: int):
    """ Compare guess and real config at some position. """
    assert real["name"] == guess["name"], f"Incorrect name in config at position {position}"
    assert real["value"] == guess["value"], f"Incorrect value of " \
        f"{real['name']} in config at position {position}"


def test_config_content(name: str, value: str, position=-1):
    """ Testing guess config content is a real value of config item.  """
    with open(CONFIG_PATH) as config:
        config_content = config.read()

    config_lines = get_config_lines(config_content)

    guess_content = get_guess_content(name, value)
    test_content = get_test_content(config_lines[position])

    compare_config_content(guess_content, test_content, position)

    success("Test of the write method")


def get_config_length():
    """ Get length of the lines in configuration file. """
    return len(get_config_lines(get_config_content()))


def test_config_length(expected: int):
    """ Testing expected length of the config is a real length. """
    config_length = len(get_config_lines(get_config_content()))
    assert config_length == expected, "Config has incorrect length after erasing or adding!"
    success("Config length tests")


def test_item_does_not_exists(name: str):
    """ Test if erased item does not exists. """
    config_lines = get_config_lines(get_config_content())

    for line in config_lines:
        assert line[:len(name)] != name, "Item exists after erasing!"

    success("Erased item existing tests")


def write_test():
    """ Testing of the write method. """
    test_parameter = "age"
    test_value = "21"
    initial_config_length = get_config_length()

    # Write name and value.
    config_writer.write(test_parameter, test_value)
    test_config_content(test_parameter, test_value)
    test_config_length(initial_config_length + 1)

    # Write object as name: value.
    config_writer.write(items={test_parameter: test_value})
    test_config_content(test_parameter, test_value)
    test_config_length(initial_config_length + 2)


def erase_test():
    """ Testing of the erase method. """
    test_parameter = "age"
    initial_config_length = get_config_length()

    config_writer.erase(test_parameter)
    test_config_length(initial_config_length - 2)
    test_item_does_not_exists(test_parameter)

    success("Test of the erase method")


@test_box
def main():
    """ Any tests for ConfigWriter. """
    write_test()
    erase_test()

    success("Config writer tests")


if __name__ == "__main__":
    main()
