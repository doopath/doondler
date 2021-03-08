""" Init script creating .doohandlerc.py file """
import os

from sys import exit
from typing import KeysView

from modules.config_prototype import ConfigPrototype
from modules.config_reader import ConfigReader
from modules.logger import logger
from modules.errors import InitializationError
from modules.paths import get_path
from modules import yuigahama


handlers = {
    "yuigahama": yuigahama.Handler
}


def take_handler(current_handler) -> str:
    """ Ask user what he wants use as a handler and return it if exists. """
    try:
        desired_handler = ask_param(current_handler)
        assert desired_handler in handlers.keys(), f"Handler with name {desired_handler} doesn't exists!"

        return desired_handler

    except AssertionError as error:
        logger.log(error)
        logger.log(f"The default handler set as current ({current_handler['default']})")

        return current_handler["default"]


def param_is_valid(param: str) -> bool:
    """ Check if parameter is valid. """
    if len(param) == 0:
        return False

    return True


def ask_param(param: dict, skip: bool=False):
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


class Config(ConfigPrototype):
    """
        A class of main doondler config.

        Attributes
        ----------
        prototype: ConfigPrototype
            A proto of the configuration file.
        user: dict
            Current user with its parameters.
        main_path: str
            A path to the config.
        copy_path: str
            A path to the config copy (looks like /home/user/.doondlerc.copy)

        Methods
        -------
        make(remake=False) -> None
            Make config file and fill it user's data.
            If remake flag was given then remake a config.
        remake() -> None
            Remake a config file.
        remove() -> None
            remove config file.
    """

    def __init__(self):
        super().__init__()
        self.user = {}
        self.main_path = get_path("config")
        self.copy_path = get_path("config-copy")
        logger.log("Created an instance of the modules.config.Config class")

    def _create_logfile(self):
        logfile = open(get_path("logs"), "w+")
        logfile.close()

    def _set_params(self):
        self.username["value"] = ask_param(self.username)
        self.home_dir["value"] = ask_param(self.home_dir)
        self.city["value"] = ask_param(self.city)
        self.handler["value"] = take_handler(self.handler)
        self.package_manager["value"] = ask_param(self.package_manager)

        logger.log("Config params (username, home_dir, city, etc...) were set at the "
                   "modules.config.Config._set_params method.")

    def _create_doondlerc(self):
        try:
            doondlerc_path = str(self.user["home_dir"]) + "/.doondlerc"

            if os.path.isfile(doondlerc_path):
                raise InitializationError("Init file already exists!")

            doondlerc = open(doondlerc_path, "w+")

            for field, value in self.user.items():
                doondlerc.write(f"{field} = {value}\n")

            doondlerc.close()
            logger.log("Config file (doondlerc) was successfully created at the "
                       "modules.config.Config._create_doondlerc method.")

        except InitializationError as error:
            logger.log(error)
            self.remake()

    def _is_valid_options(self, options: list, to_dos: KeysView) -> bool:
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

    def _reassign_params(self, options: list):
        try:
            to_dos = {
                "snn": lambda: ask_param(self.username),
                "snh": lambda: ask_param(self.home_dir),
                "snc": lambda: ask_param(self.city),
                "cnh": lambda: ask_param(self.handler),
                "snp": lambda: ask_param(self.package_manager),
                "exit": lambda: exit()
            }

            assert self._is_valid_options(options, to_dos.keys()) is True,\
                "You gave incorrect parameters to reinitialize!"

            for option in options:
                to_dos[option]()

            logger.log("Config params were reassigned.")

        except AssertionError as error:
            logger.log(error)
            exit()

    def _set_local_params(self):
        local_config = ConfigReader(self.copy_path)
        local_config = local_config.read()

        for param, value in local_config.items():
            self.user[param] = value

    def _create_user(self):
        self.user["username"] = self.username["value"] or self.user["username"]
        self.user["home_dir"] = self.home_dir["value"] or self.user["home_dir"]
        self.user["city"] = self.city["value"] or self.user["city"]
        self.user["handler"] = self.handler["value"] or self.user["handler"]
        self.user["package_manager"] = self.package_manager["value"] or self.user["package_manager"]

    def _show_reinit_options(self):
        print("Options: \n"
              "  exit - exit without changes\n"
              "  snn - set new name\n"
              "  snh - set new home_dir\n"
              "  snc - set new city\n"
              "  cnh - choose new handler\n"
              "  snp - set new package manager\n")

    def _prepare_reinit_options(self, input_line: str) -> list:
        options = input_line.strip().strip("<").strip(">")
        split_options = list(map(lambda item: item.strip(), options.split(",")))

        return split_options if len(split_options) > 0 else [options]

    def _make_copy(self):
        config_path = self.main_path
        config_copy_path = self.copy_path

        if not os.path.isfile(config_path):
            raise FileExistsError("Config does not exist!")

        with open(config_path) as config:
            with open(config_copy_path, "w+") as config_copy:
                config_copy.write(config.read())

    def _remove_copy(self):
        config_copy_path = self.copy_path

        if not os.path.isfile(config_copy_path):
            raise FileExistsError("Config copy does not exist!")

        os.remove(config_copy_path)

    def _reinit(self):
        self._show_reinit_options()

        options = input('Please, take a few options like <cnh, snc, snn>: ')
        options = self._prepare_reinit_options(options)

        self._reassign_params(options)
        self._set_local_params()
        self._create_user()
        self._create_doondlerc()

        print("\n☑ You have successfully initialized!")

    def make(self, remake=False):
        """ Make a config file (~/.doondlerc). """
        if remake:
            logger.log("Starting reinitialization process at the modules.config.Config"
                       ".make method.")
            self._reinit()
            self._remove_copy()
            exit()

        print(f"Hello, {self.username['default']}!")

        self._set_params()
        self._create_user()
        self._create_logfile()
        self._create_doondlerc()

        print("\n☑ You have successfully initialized!")
        logger.log("The user has passed the initialization successfully at the "
                   "modules.config.Config.make method.")
        exit()

    def remove(self):
        """ Remove a config file. """
        is_config_exists = os.path.isfile(self.main_path)
        assert is_config_exists, "You cannot remove file that not exists!"

        os.remove(self.main_path)
        logger.log("The config has been removed successfully at the modules.config"
                   ".Config.remove method.")

    def remake(self):
        """ Remake a configuration file. """
        print("\n✘ Oops, seems like there is raised the InitializationError!\n")
        print("Variants: \n"
              "1 - reinitialize;\n"
              "2 - exit;\n")
        answ = input("What you want to do?: ")
        print("\n")

        if answ == "1":
            self._make_copy()
            self.remove()
            self.make(remake=True)
        else:
            print("Goodbye! But, anyway, try to init later! 🖐")
            logger.log("Remake prccess has been interrupted at the modules.config.Config"
                       ".remake method.")
            exit()
