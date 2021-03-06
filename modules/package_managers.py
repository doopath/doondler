""" A module of system pocket managers. """
import os
import distro

from sys import exit

from modules.logger import logger


class PackageManager:
    """
        An abstract class of system pocket manager.

        Attributes
        ----------
        name: str
            Name of pocket manager.

        Methods
        -------
        install(program: str)
            Install program.
        uninstall(program:str, dependencies(for pacman based))
            Uninstall program (with or without dependencies.
        sys_update()
            Update system and packages.
    """
    name = "PackageManager"

    def install(self, program: str):
        """ Install program. """

    def uninstall(self, program: str):
        """ Uninstall program. """

    def sys_update(self):
        """ Update system and packages. """


class Pacman(PackageManager):
    """
        A class of Pacman.
        Pacman is a default arch-based package manager.
        You can see more about it here: https://wiki.archlinux.org/index.php/pacman
    """
    name = "pacman"

    def install(self, program: str):
        os.system(f"sudo pacman -S {program}")

    def uninstall(self, program: str):
        """ Uninstall program with or without dependencies. """
        dependencies = input(
            f"Do you want to uninstall all dependencies with {program}? (y/n): ").lower()

        if dependencies == "y":
            print("Warning: Check if it's safe. You can uninstall needed dependencies.")
            os.system(f"sudo yay -Rsn {program}")
        elif dependencies == "n":
            os.system(f"sudo yay -Rdn {program}")
        else:
            print("You should answer y or n!\n")
            self.uninstall(program)

    def sys_update(self):
        os.system("sudo pacman -Suy")


class Apt(PackageManager):
    name = "apt"

    def install(self, program: str):
        os.system(f"sudo apt-get install {program}")

    def uninstall(self, program: str):
        os.system(f"sudo apt remove {program}")

    def sys_update(self):
        os.system("sudo apt-get update && sudo apt-get upgrade")


class Dnf(PackageManager):
    name = "dnf"

    def install(self, program: str):
        os.system(f"dnf install {program}")

    def uninstall(self, program: str):
        os.system(f"dnf remove {program}")

    def sys_update(self):
        """ Unable method. """
        print("Sorry, but now you cannot use this option. Doondler don't knows how to "
              "update your system, so if you want to do it you can create an issue on github"
              "P.S: You can do it here: https://github.com/doopath/doondler/issues")
        exit()


class Yay(PackageManager):
    name = "yay"

    def install(self, program: str):
        os.system(f"sudo yay -S {program}")

    def uninstall(self, program: str):
        """ Uninstall program with or without dependencies. """
        dependencies = input(
            f"Do you want to uninstall all dependencies with {program}? (y/n): ").lower()
        if dependencies == "Y":
            print("Warning: Check if it's safe. You can uninstall needed dependencies.")
            os.system(f"sudo yay -Rsn {program}")
        elif dependencies == "N":
            os.system(f"sudo yay -Rdn {program}")
        else:
            print("You should answer y or n!\n")
            self.uninstall(program)

    def sys_update(self):
        os.system("sudo yay -Suy")


class Yaourt(PackageManager):
    name = "yaourt"

    def install(self, program: str):
        os.system(f"sudo yaourt -S {program}")

    def uninstall(self, program: str, dependencies=False):
        if dependencies:
            print("Warning: Check if it's safe. You can uninstall required dependencies.")
            os.system(f"sudo yaourt -Rsn {program}")
        else:
            os.system(f"sudo yaourt -Rdn {program}")

    def sys_update(self):
        os.system("sudo yaourt -Suy")


def get_managers():
    """ Get available package managers. """
    return {
        "apt": Apt,
        "pacman": Pacman,
        "dnf": Dnf,
        "yay": Yay,
        "yaourt": Yaourt
    }


def get_couples():
    """ Get  couples of system_name: package_manager. """
    return {
        "arch": Pacman,
        "ubuntu": Apt,
        "fedora": Dnf,
        "arcolinux": Pacman,
        "linuxming": Apt
    }


def get_package_manager(manager_name: str):
    """ Create a pocket manager. """
    try:
        managers = get_managers()
        pocket_manager = managers[manager_name]

        assert manager_name in managers, f"Package manager with name: {manager_name} doesn't exits!"

        return pocket_manager

    except AssertionError as error:
        logger.log(error)
        exit()


class DefaultManager:
    """
        Select a default package manager.

        Attributes
        ----------
        couples: dict { "system": Manager } - 
            Couples of system name and package managers.\n
        managers: dict { "name": Manager } - 
            Available package managers.

        Methods
        -------
        get_default_manager() - 
            Returns a class as your default package manager.
    """

    def __init__(self):
        self.couples = get_couples()
        self.managers = get_managers()

    def _show_managers(self):
        for manager in self.managers:
            print(f"--- {manager}\n")

    def _check_if_manager_exists(self, manager: str):
        try:
            assert manager in self.managers, "Chosen manager is not supported!"

        except AssertionError as error:
            logger.log(error)
            exit()

    def get_default_manager(self):
        """ Get default package manager. """
        current_distro = distro.id()

        if current_distro not in self.couples:
            print("Sorry, but we cannot recognize your package manager. Now you cannot use a few of features."
                  "But we support these managers: ")
            self._show_managers()

            manager = input("Please, choose one of them: ")
            self._check_if_manager_exists(manager)

            return self.managers[manager]

        return self.couples[current_distro]
