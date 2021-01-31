""" Init script creating .doohandlerc.py file """
import os
from sys import exit  # Necessary to pyinstaller building

from modules.config_prototype import ConfigPrototype
from modules.logger import Logger
from modules.errors import InitializationError
from modules.paths import get_path
from modules import yuigahama

handlers = [yuigahama.Handler]
logger = Logger(".doondler_logs")


def get_handlers():
    """ Get list of handlers to show it to user. """
    if len(handlers) < 2:
        return False

    res = ""
    i = 0

    while i < len(handlers):
        res += f"{i + 1} = {handlers[i].name}\n"
        i += 1

    return res


def get_handler(id: int):
    try:
        assert len(handlers) - 1 >= id, f"Handler with id={id} doesn't exists!"

        return handlers[id]

    except AssertionError as error:
        logger.log(error)
        exit()


def param_is_valid(param: str):
    """ Check if parameter is valid. """
    if len(param) == 0:
        return False

    return True


def ask_param(param: dict, skip=False):
    """ Ask a value to user. """
    try:
        answ = input(param["main_question"] + " (y/n): ").upper()

        if answ == "Y":
            if not skip:
                param["value"] = input(param["confirm_question"] + ": ")
                assert param_is_valid(param["value"]) is True, "You gave incorrect parameter!"

                return param["value"]

            print(param["confirm_quest"])

        elif answ != "N":
            param["main_question"] = "Please, answer y or n"
            ask_param(param)

        return param["default"]

    except AssertionError as error:
        logger.log(error)
        exit()


class Config:
    """
        A class of main doondler config.

        Attributes
        ----------
        prototype: ConfigPrototype
            A proto of the configuration file.
        user: dict
            Current user with its parameters.

        Methods
        -------
        make(remake=False)
            Make config file and fill it user's data.
            If remake flag was given then remake a config.
        remake()
            Remake a config file.
        remove()
            remove config file.
    """

    def __init__(self):
        self.user = {}
        self.prototype = ConfigPrototype()

    def _create_logfile(self):
        logfile = open(get_path("logs"), "w+")
        logfile.close()

    def _set_params(self):
        self.prototype.username["value"] = ask_param(self.prototype.username)
        self.prototype.home_dir["value"] = ask_param(self.prototype.home_dir)
        self.prototype.city["value"] = ask_param(self.prototype.city)
        self.prototype.handler["value"] = ask_param(self.prototype.handler)
        self.prototype.package_manager["value"] = ask_param(self.prototype.package_manager)

    # def _set_handler(self):
    #     handlers_choice = get_handlers()
    #
    #     if handlers_choice:
    #         handlers_choice = "\n" + handlers_choice + "\nOk, then select one of these (default=1)"
    #
    #     handler_id = ask_param(
    #         f"Do you want to change you daemon-handler or keep default={self.handler.name}?",
    #         handlers_choice or "Sorry, but now only one handler can help you.",
    #         1,
    #         skip=not bool(handlers_choice)
    #     ) or 0
    #
    #     if handler_id:
    #         handler_id = int(handler_id) - 1
    #
    #     self.handler = get_handler(handler_id)

    def _create_doondlerc(self):
        try:
            doondlerc_path = str(self.user["home_dir"]) + "/.doondlerc"

            if os.path.isfile(doondlerc_path):
                raise InitializationError("Init file already exists!")

            doondlerc = open(doondlerc_path, "w+")

            for field, value in self.user.items():
                doondlerc.write(f"{field} = {value}\n")

            doondlerc.close()

        except InitializationError as error:
            logger.log(error)
            self.remake()

    def _is_valid_options(self, options, to_dos):
        if len(options) < 1:
            return False

        for option in options:
            if option == "exit" and len(options) > 1:
                return False
            elif option not in to_dos:
                return False

            for suboption in options:
                if suboption == options and options.index(suboption) != options.index(options):
                    return False

        return True

    def _reassign_params(self, options):
        try:
            to_dos = {
                "snn": lambda: ask_param(self.prototype.username),
                "snh": lambda: ask_param(self.prototype.home_dir),
                "snc": lambda: ask_param(self.prototype.city),
                "cnh": lambda: ask_param(self.prototype.handler),
                "snp": lambda: ask_param(self.prototype.package_manager),
                "exit": lambda: exit()
            }

            assert self._is_valid_options(options, to_dos.keys()) is True, "You gave incorrect parameters to reinitialize!"

            for option in options:
                to_dos[option]()

        except AssertionError as error:
            logger.log(error)
            exit()

    def _create_user(self):
        for _name, _value in self.prototype.__dict__.items():
            self.user[_name] = _value["value"]

    def _show_reinit_options(self):
        print("Options: \n"
              "  exit - exit without changes\n"
              "  snn - set new name\n"
              "  snh - set new home_dir\n"
              "  snc - set new city\n"
              "  cnh - choose new handler\n"
              "  snp - set new package manager\n")

    def _reinit(self):
        self._show_reinit_options()

        options = input('Please, take a few options like <cnh, snc, snn>: ')
        options = options.strip().strip("<").strip(">")
        options = options.split(",")

        self._reassign_params(options)
        self._create_user()
        self._create_doondlerc()

        print("\n☑ You have successfully initialized!")
        exit()

    def make(self, remake=False):
        """ Make a config file (~/.doondlerc). """
        if remake:
            self._reinit()
            exit()

        print(f"Hello, {self.prototype.username['default']}!")

        self._set_params()
        self._create_user()

        self._create_logfile()
        self._create_doondlerc()

        print("\n☑ You have successfully initialized!")
        exit()

    def remove(self):
        """ Remove a config file. """
        is_config_exists = os.path.isfile(get_path("config"))
        assert is_config_exists, "You cannot remove file that not exists!"

        os.remove(get_path("config"))

    def remake(self):
        """ Remake a configuration file. """
        print("\n✘ Oops, seems like there is raised the InitializationError!\n")
        print("Variants: \n"
              "1 - reinitialize;\n"
              "2 - exit;\n")
        answ = input("What you want to do?: ")
        print("\n")

        if answ == "1":
            self.remove()
            self.make(remake=True)
        else:
            print("Goodbye! But, anyway, try to init later! 🖐")
            exit()
