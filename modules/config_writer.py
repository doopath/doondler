""" Write key = value to a config file """
import os
import sys

from modules.config_reader import ConfigReader
from modules.logger import logger
from modules.paths import get_path


class ConfigWriter:
    """
        A class used to write or erase something to/from configuration file.

        Attributes
        ----------
        path: str
            Location of a configuration file; default = get_path("config").
        config_reader: ConfigReader
            The class needs to read config for erasing from it.

        Methods
        -------
        write(name=None, value=None, items=None)
            Write a couple name = value or items({ name: value }) to the config.
        erase(name=None, names=None)
            Erase attribute(name) or attributes(names) from the config.
    """

    def __init__(self, path=get_path("config")):
        self.path = path
        self.config_reader = ConfigReader(self.path)
        logger.log("Created an instance of the modules.config_writer.ConfigWriter class.")

    def _create_config_item(self, key, value):
        try:
            assert bool(key) is True, "You cannot set empty parameter name!"
            assert bool(value) is True, "You cannot set empty parameter value!"

            return f"{key} = {value}\n"

        except AssertionError as e:
            logger.log(e)
            sys.exit()

    def _write_par_to_config(self, config, name: str, value: str):
        config_item = self._create_config_item(name, value)
        config.write(config_item)

    def _write_items_to_config(self, config, items: dict):
        try:
            assert len(items.keys()) != 0, "You cannot set empty list of parameters!"

            for name, value in items.items():
                self._write_par_to_config(config, name, value)

        except AssertionError as e:
            logger.log(e)
            sys.exit()

    def _erase_items(self, config_content, names):
        for name in names:
            assert name in config_content is not False, "You cannot delete item which not exists!"
            del config_content[name]

            return config_content

    def _check_if_given_both(self, name, names):
        assert not (name and names), "You can give either name or names parameter, but not both!"

    def write(self, name=None, value=None, items=None):
        """
            Write element to a config.

            Arguments
            ---------
            name: str
                Name of a config attribute.
            value: str
                Value of a config attribute.
            items: dict { "name" : "value" }
                A dictionary of couples name: value. Any Items will be written to a config.
        """
        try:
            assert os.path.isfile(self.path), "Config file does not exists!"

            config = open(self.path, "a")
            self._write_items_to_config(config, items or {name: value})
            config.close()

            logger.log("The param(s) ha(s/ve) been written to the config.")

        except AssertionError as error:
            logger.log(error)
            sys.exit()

    def erase(self, name=None, names=None):
        """
            Erase element or elements from a config.

            Attributes
            ----------
            name: str
                Name of an erasing element.
            names: list [ "name", "name" ]
                List of names those should be erased.
        """
        config = open(self.path, "r")
        config_backup = self.config_reader.read()
        config_content = self.config_reader.read()
        config.close()

        try:
            self._check_if_given_both(name, names)

            config = open(self.path, "w")
            config_content = self._erase_items(config_content, names or [name])
            self._write_items_to_config(config, config_content or {})
            config.close()

            logger.log("The param(s) ha(s/ve) been erased from the config.")

        except AssertionError as e:
            config_writer.write(items=config_backup)
            logger.log(e)
            sys.exit()
