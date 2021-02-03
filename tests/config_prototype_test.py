""" Testing of the config_prototype module. """
from tests.success import success
from tests.test_box import test_box

from modules.config_prototype import ConfigPrototype


def test_parameters():
    """ Testing of config_prototype parameters. """
    prototype = ConfigPrototype()

    assert all("" == p["value"] for p in prototype.__dict__.values()), "" \
        "Prototype parameter's value can only be equals \"\"!"
    assert all("" != p["default"] for p in prototype.__dict__.values()), "" \
        "Prototype parameter's default value cannot be equals \"\"!"
    assert all("" != p["main_question"] for p in prototype.__dict__.values()), "" \
        "Prototype parameter's main_question cannot be equals \"\"!"
    assert all("" != p["confirm_question"] for p in prototype.__dict__.values()), "" \
        "Prototype parameter's confirm_question cannot be equals \"\"!"

    success("Parameters test")


@test_box
def main():
    """ Main function of the config prototype tests. """
    test_parameters()


if __name__ == "__main__":
    main()
