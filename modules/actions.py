""" Available program commands. """
from modules import yuigahama
from modules.user import User
from modules.package_managers import get_pocket_manager
from modules.config import Config
from modules.help import show_help_list
from modules.password_generator import gen_password
from modules.version_info import get_version_info
from modules.synoptic import Synoptic

from tests.test_mock import test1_mock, test2_mock


user = User()
user.create()

handlers = {
    "yuigahama": yuigahama.Handler
}

pocket_manager = get_pocket_manager(user.pocket_manager)()
handler = handlers[user.handler](user)

actions = {
    "--help": {
        "action": show_help_list,
        "arguments": 0,
        "option": "--help"
    },
    "--version": {
        "action": show_version_info,
        "arguments": 0,
        "option": "--version"
    },
    "-test1": {
        "action": test1_mock,
        "arguments": 1,
        "option": "-test1"
    },
    "--test2": {
        "action": test2_mock,
        "arguments": 0,
        "option": "--test2"
    },
    "--make-note": {
        "action": handler.make_note,
        "arguments": 2,
        "option": "--make-note"
    },
    "-reinit": {
        "action": Config().remake,
        "arguments": 0,
        "option": "-reinit"
    },
    "-install": {
        "action": pocket_manager.install,
        "arguments": 1,
        "option": "-install"
    },
    "-i": {
        "action": pocket_manager.install,
        "arguments": 1,
        "option": "-i"
    },
    "-uninstall": {
        "action": pocket_manager.uninstall,
        "arguments": 1,
        "option": "-uninstall"
    },
    "--sys-update": {
        "action": pocket_manager.sys_update,
        "arguments": 0,
        "option": "--sys-update"
    },
    "-su": {
        "action": pocket_manager.sys_update,
        "arguments": 0,
        "option": "-su"
    },
    "--gen-password": {
        "action": gen_password,
        "arguments": 2,
        "option": "--gen-password"
    },
    "-gp": {
        "action": gen_password,
        "arguments": 2,
        "option": "-gp"
    },
    "-weather": {
        "action": Synoptic().get_weather,
        "arguments": 0,
        "option": "-weather"
    }
}
