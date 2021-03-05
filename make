#! /usr/bin/python3
""" Build script for doondler sources """

import os
import sys
import shutil


paths = {
    "main_name": "main.py",
    "target_name": "doondler",
    "build_tool": "pyinstaller",
    "built_binary_pyinstaller": "./dist/pyinstaller/doondler",
    "built_binary_nuitka": "./dist/nuitka/doondler",
}


class Builder:
    """
        A class of a project builder.

        Attributes
        ----------
        main_source: str
            A name of a main file of the project.
        target: str
            A name of a target binary.
        build_tool: str
            A tool for project building.

        Methods
        -------
        build(): void
            build the project.
    """

    def __init__(self):
        self.main_source = paths["main_name"]
        self.target = paths["target_name"]
        self.build_tool = paths["build_tool"]

    def _remove_pyinstaller_buildings(self):
        shutil.rmtree("build")
        shutil.rmtree("__pycache__")
        os.remove(self.target + ".spec")

        if not os.path.isdir("./dist/pyinstaller"):
            os.mkdir("./dist/pyinstaller")

        if os.path.isfile(f"./dist/pyinstaller/{self.target}"):
            os.remove(f"./dist/pyinstaller/{self.target}")

        shutil.move("./dist/" + self.target, "./dist/pyinstaller/")

    def _remove_nuitka_buildings(self):
        os.rename(self.main_source.split(".")[0] + ".bin", self.target)

        if not os.path.isdir("./dist"):
            os.mkdir("dist")
        if not os.path.isdir("./dist/nuitka"):
            os.mkdir("./dist/nuitka")

        if os.path.isfile(f"./dist/nuitka/{self.target}"):
            os.remove(f"./dist/nuitka/{self.target}")

        shutil.move(self.target, "dist/nuitka")

    def _remove_buildings(self):
        if self.build_tool == "pyinstaller":
            self._remove_pyinstaller_buildings()
        elif self.build_tool == "nuitka":
            self._remove_nuitka_buildings()

    def _nuitka_build(self):
        os.system(f"python3 -m nuitka --follow-imports --plugin-enable=pylint-warnings {self.main_source}")

    def _pyinstaller_build(self):
        os.system(f"python3 -m PyInstaller --onefile {self.main_source} -n {self.target}")

    def build(self):
        """ Make a binary with the build tool and delete rest. """
        print("\n")

        if self.build_tool == "pyinstaller":
            self._pyinstaller_build()
        elif self.build_tool == "nuitka":
            self._nuitka_build()

        self._remove_buildings()
        print("Project was built successfully!")


class Installer:
    """
        A class of a built binary installer.

        Attributes
        ----------
        build_tool: str
            A tool for project building.

        Methods
        -------
        install()
            Install a built binary file.
    """

    def __init__(self):
        self.build_tool = paths["build_tool"]

    def _ask_user(self):
        answer = input("Do you want to install the binary to the /usr/bin path? (y/n): ").lower()

        if answer == "n":
            print("Ok, so goodbye!")
            sys.exit()
        elif answer != "n" and answer != "y":
            print("Please, answer y or n!")
            self._ask_user()

        return True

    def _check_binary_existence(self):
        assert os.path.isfile(paths["built_binary_"+self.build_tool]), "The binary doesn't exists! Please, build" \
            " project and after all install a binary."

        return True

    def install(self):
        """ Install a built binary. """
        if self._ask_user() and self._check_binary_existence():
            os.system(f"sudo cp {paths['built_binary_'+self.build_tool]} /usr/bin/")
            print("The program was successfully installed!")


def ask_info(param_name):
    """ Ask some parameter value to user. """
    try:
        answer = input(f"Please, enter the {param_name} name: ")

        assert len(answer) > 0, ask_info(f"correct {param_name}")

        return answer
    except AssertionError as e:
        print(e)
        sys.exit()


def install_pyinstaller():
    """ Install the pyinstaller build tool. """
    if os.path.isfile("/usr/bin/pyinstaller") is False:
        answer = input("The path /usr/bin/ doest not contains a pyinstaller binary,"
                       " did you install it or install now? (y/n): ")

        if answer.lower() == "y":
            pip = input("What is your python3 pip binary name (for example: pip3 in debian): ")
            os.system(f"{pip} install pyinstaller")
            os.system("sudo cp ~/.local/bin/pyinstaller /usr/bin/")
        elif answer.lower() != "y" and answer.lower() != "n":
            print("Please, answer y or n!")
            install_pyinstaller()
    else:
        print("Pyinstaller is already installed! Nothing to do.")


def install_dependencies():
    """ Install all dependencies. """
    pip = input("What is your python3 pip binary name (for example: pip3 on debian): ")
    os.system(f"{pip} install -r requirements.txt")

    print("All of requirements are successfully installed!")


def install_pip():
    os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    os.system("python3 get-pip.py")
    os.system("rm ./get-pip.py")

    print("Pip3 was successfully installed!")


if __name__ == "__main__":
    if "-dev" in sys.argv:
        paths["main_name"] = ask_info("building python file")
        paths["target_name"] = ask_info("building file")

    if "-nuitka" in sys.argv:
        paths["build_tool"] = "nuitka"

    elif "-pyinstaller" in sys.argv:
        paths["build_tool"] = "pyinstaller"

    if "-pip" in sys.argv:
        install_pip()

    if "-pi" in sys.argv:
        install_pyinstaller()

    if "-deps" in sys.argv:
        install_dependencies()

    if "-b" in sys.argv:
        Builder().build()

    if "-i" in sys.argv:
        Installer().install()
