""" A module for generating a random password."""
import random
import string

from sys import exit
from pyperclip import copy as copy_to_clip

from modules.logger import logger
from modules.colors import to_green


class PasswordGenerator:
    """
        A class of a password generator.

        Properties
        ----------
        _pass_prefix: str
            A prefix for password. Needed for better unique of generated password.
            For example: fIreFOxa12ljLKl
        _pass_length: int
            Length of main part of a password (length without prefix).
        _letters_list: list
            A list of ascii letters and numbers.

        Methods
        -------
        gen_password(): str
            Returns a generated password.
    """

    def __init__(self, pass_prefix: str, pass_length: int):
        self._pass_prefix = pass_prefix.lower()
        self._pass_length = pass_length + 1
        self._letters_list = []

    def _set_letters_list(self):
        self._letters_list += [x for x in string.ascii_letters]
        self._letters_list += [str(x) for x in string.digits]
        self._letters_list += ["_", "!", "?", "-", "&", "$"]

    def _set_pass_prefix(self):
        result = ""

        for i in self._pass_prefix:
            result += i.lower() if random.randint(0, 10) < 4 else i.upper()

        self._pass_prefix = result

    def gen_password(self):
        """ Generate a random password. """
        self._set_letters_list()
        self._set_pass_prefix()

        result = self._pass_prefix

        for i in range(self._pass_length):
            result += random.choice(self._letters_list)

        return result


def gen_password(prefix: str, length: str):
    """ Generate a random password with set length and print it. """
    try:
        password_generator = PasswordGenerator(prefix, int(length))
        password = password_generator.gen_password()

        print(f"\n{to_green('A password was successfully generated!')}\nResult: {password}")
        print("Copied to the clipboard.\n")
        copy_to_clip(password)

    except Exception as error:
        logger.log(error)
        exit()
