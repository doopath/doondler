""" Init script creating .doohandlerc.py file """
import os
import getpass
from sys import exit  # Necessary to pyinstaller building

from modules.logger import Logger
from modules.errors import InitializationError
from modules.paths import get_path
from modules.config_sample import config_sample
from modules.package_managers import DefaultManager
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


def ask_param(main_quest: str, confirm_quest: str, default, skip=False):
    """ Ask a value to user. """
    try:
        answ = input(main_quest + " (y/n): ").upper()

        if answ == "Y":
            if not skip:
                param = input(confirm_quest + ": ")
                assert param_is_valid(param) is True, "You gave incorrect parameter!"

                return param

            print(confirm_quest)

        elif answ != "N":
            ask_param("Please, answer y or n", confirm_quest, default)

        return default

    except AssertionError as error:
        logger.log(error)
        exit()


class Config:
    """
        A class of main doondler config.

        Attributes
        ----------
        username: str
            Name of currenct PC user.
        home_dir: str
            Currect home directory.
        city: str
            User's city.
        handler: Handler
            Handler selected by user.
        user: dict
            Currect user with its parameters.

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
        self.username = getpass.getuser()
        self.home_dir = get_path("home")
        self.city = "moscow"
        self.handler = yuigahama.Handler
        self.pocket_manager = DefaultManager().get_default_manager().name
        self.user = {}

    def _create_logfile(self):
        logfile = open(get_path("logs"), "w+")
        logfile.close()

    def _set_username(self):
        self.username = ask_param(
            f"Do you want to change your name to call you or keep default={self.username}?",
            "Ok, then enter a new name",
            self.username
        )

    def _set_home_dir(self):
        self.home_dir = ask_param(
            f"Do you want to change your home dir or keep default={self.home_dir}?",
            "Ok, then enter a path",
            self.home_dir
        )

    def _set_pocket_manager(self):
        self.pocket_manager = ask_param(
            f"Do you want to change your pocket_manager default={self.pocket_manager}?",
            "Ok, then enter a name:",
            self.pocket_manager
        )

    def _set_city(self):
        self.city = ask_param(
            f"Do you want to change you city or keep default={self.city}?",
            'Ok, then enter a city like <nizhniy-novgorod>',
            self.city
        ).lower().strip("<").strip(">")

    def _set_handler(self):
        handlers_choice = get_handlers()

        if handlers_choice:
            handlers_choice = "\n" + handlers_choice + "\nOk, then select one of these (default=1)"

        handler_id = ask_param(
            f"Do you want to change you daemon-handler or keep default={self.handler.name}?",
            handlers_choice or "Sorry, but now only one handler can help you.",
            1,
            skip=not bool(handlers_choice)
        ) or 0

        if handler_id:
            handler_id = int(handler_id) - 1

        self.handler = get_handler(handler_id)

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
            if option == "kcp" and len(options) > 1:
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
                "snn": self._set_username,
                "snh": self._set_home_dir,
                "snc": self._set_city,
                "cnh": self._set_handler,
                "kcp": self._create_doondlerc
            }

            assert self._is_valid_options(options, to_dos) is True, ("""You 
                give incorrect parameters to reinitialize!""")

            if "kcp" not in options:
                for option in options:
                    to_dos[option]()

        except AssertionError as error:
            logger.log(error)
            exit()

    def _create_user(self):
        self.user = config_sample
        self.user["name"] = self.username
        self.user["home_dir"] = self.home_dir
        self.user["city"] = self.city
        self.user["handler"] = self.handler.name
        self.user["pocket_manager"] = self.pocket_manager

    def _show_reinit_options(self):
        print("Options: \n"
              "  snn - set new name\n"
              "  snh - set new home_dir\n"
              "  snc - set new city\n"
              "  cnh - chose new handler\n"
              "  kcp - keep current params\n")

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

        print(f"Hello, {self.username}!")

        self._set_username()
        self._set_home_dir()
        self._set_city()
        self._set_handler()

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
