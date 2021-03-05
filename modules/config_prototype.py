""" A configuration file prototype module. """
import getpass

from modules.paths import get_path
from modules import yuigahama
from modules.package_managers import DefaultManager


class ConfigPrototype:
    """
        A class of a configuration file prototype.
        Here you can find and add some options and attributes.
        Every filling parameter should has value (usually is empty), main question
        (a question that be ask to user for his value), confirm question (when user
        said "y" to a main question and wants to type its value and default value
        of a parameter that be use if user answered "n" to a main question.

        There is docs:

        Attributes
        ----------
        default: dict
            Default parameters for others.
        username: str
            User's name or what his chose to call him.
        home_dir: str
            A path to user's home directory.
        city: str
            Where is user location.
        handler: Handler type object
            A system handler.
        package_manager: str
            Using by user package manager, for example on Debian based distributions: apt; or
            pacman on ArchLinux.
    """

    def __init__(self):
        self.default = {
            "username": getpass.getuser(),
            "home_dir": get_path("home"),
            "city": "moscow",
            "handler": yuigahama.Handler,
            "package_manager": DefaultManager().get_default_manager().name
        }
        self.username = {
            "value": "",
            "main_question": f"Do you want to change your name to call you or keep default={self.default['username']}?",
            "confirm_question": "Ok, then enter a new name",
            "default": self.default["username"]
        }
        self.home_dir = {
            "value": "",
            "main_question": f"Do you want to change your home dir or keep default={self.default['home_dir']}?",
            "confirm_question": "Ok, then enter a path",
            "default": self.default["home_dir"]
        }
        self.city = {
            "value": "",
            "main_question": f"Do you want to change your home dir or keep default={self.default['city']}?",
            "confirm_question": "Ok, so enter your city like <los-angeles> or <nizhny-novgorod>",
            "default": self.default["city"]
        }
        self.handler = {
            "value": "",
            "main_question": f"Do you want to change your home dir or keep default={self.default['handler'].name}?",
            "confirm_question": "Ok, then enter a handler's name",
            "default": self.default["handler"].name
        }
        self.package_manager = {
            "value": "",
            "main_question": f"Do you want to change your package manager or keep default={self.default['package_manager']}?",
            "confirm_question": "Ok, then enter your package manager",
            "default": self.default["package_manager"]
        }
        del self.__dict__["default"]

