""" Read and handle a config file """
import os
import sys

from modules.logger import logger
from modules.errors import InitializationError
from modules.paths import get_path


class ConfigReader:
    """ Config reader module. """
    def __init__(self, path=None):
        self.path = path or get_path("config")

    def _get_config_content(self):
        try:
            if not os.path.isfile(self.path):
                raise InitializationError("Oops! Config reader cannot find config file!")

            config = open(self.path, "r")
            config_content = config.read()
            config.close()

            return config_content

        except InitializationError as error:
            logger.log(error)
            sys.exit()

    def _map_config_items(self, config_item):
        config_item = config_item.strip()

        if config_item != "":
            return config_item

    def _filter_config_items(self, config_item):
        if config_item is not None:
            return True

    def _create_config_items(self, config_content):
        try:
            assert config_content != "", "Config reader said your config is empty!"

            config_items = config_content.split("\n")
            config_items = list(map(self._map_config_items, config_items))
            config_items = list(filter(self._filter_config_items, config_items))

            assert len(config_items) != 0, "No one valid element in your config file!"

            return config_items

        except AssertionError as error:
            logger.log(error)
            sys.exit()

    def _create_config_item(self, item):
        params = item.split("=")
        params[0] = params[0][:-1].replace(" ", "-")
        params[1] = params[1][1:].replace(" ", "-")

        return params

    def _create_config(self, config_items):
        config_items = list(map(self._create_config_item, config_items))
        config = {}

        for item in config_items:
            config[item[0]] = item[1]

        return config

    def read(self) -> dict:
        """ Read content of the configuration file. """
        config_content = self._get_config_content()
        config_items = self._create_config_items(config_content)
        config = self._create_config(config_items)

        return config


