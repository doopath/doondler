""" Available program parameters. """
from modules import yuigahama
from modules.user import User
from modules.package_managers import get_package_manager

from modules.config import Config
from modules.help import show_help_list
from modules.password_generator import gen_password
from modules.version_info import show_version_info
from modules.synoptic import Synoptic
from modules.performance_handler import PerformanceHandler
from modules.sea_battle.render import beta_render

# Using to test this and action_handler module.
from tests.test_mock import test1_mock, test2_mock


user = User()
user.create()

handlers = {
    "yuigahama": yuigahama.Handler
}

package_manager = get_package_manager(user.package_manager)()
handler = handlers[user.handler](user)

actions = {
    "--init": {
        "action": Config().make,
        "arguments": 0,
        "option": "--init"
    },
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
        "action": package_manager.install,
        "arguments": 1,
        "option": "-install"
    },
    "-i": {
        "action": package_manager.install,
        "arguments": 1,
        "option": "-i"
    },
    "-uninstall": {
        "action": package_manager.uninstall,
        "arguments": 1,
        "option": "-uninstall"
    },
    "--sys-update": {
        "action": package_manager.sys_update,
        "arguments": 0,
        "option": "--sys-update"
    },
    "-su": {
        "action": package_manager.sys_update,
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
    },
    "--performance-boost": {
        "action": PerformanceHandler().boost,
        "arguments": 0,
        "option": "--performance-boost"
    },
    "--performance-powersave": {
        "action": PerformanceHandler().powersave,
        "arguments": 0,
        "option": "--performance-powersave"
    },
    "--sea-battle-render-beta": {
        "action": beta_render,
        "arguments": 0,
        "option": "--sea-battle-render-beta"
    }
}
