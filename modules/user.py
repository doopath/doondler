""" There is basic user info """
import os
import sys

from modules.config_reader import ConfigReader
from modules.logger import logger
from modules.paths import get_path
from modules.errors import *

home = get_path("home")
config_reader = ConfigReader(get_path("config"))


def check_if_config_exists():
    """ Check if required configuration file exists. """
    if not os.path.isfile(get_path("config")):
        logger.log(Warning(
            "✘ You haven't initialized! Execute doondler --init to create a"
            " user config file and continue!"))
        raise InitializationError(
            "Initialization error! Initialize and try again!")


class User:
    """ Main user class """

    def __init__(self):
        self.username = ""
        self.city = ""
        self.home_dir = ""
        self.handler = ""
        self.package_manager = ""

    def change_par(self, par_name, new_par):
        """ Change user's parameter """
        self.__dict__[par_name] = new_par

    def create(self):
        """ Create a user """
        try:
            check_if_config_exists()

            user_ = config_reader.read()
            self.username = user_["username"]
            self.city = user_["city"]
            self.home_dir = user_["home_dir"]
            self.handler = user_["handler"]
            self.package_manager = user_["package_manager"]
            self.__dict__ = user_

        except InitializationError as error:
            logger.log(error)
            sys.exit()
