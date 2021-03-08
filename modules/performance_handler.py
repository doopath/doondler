"""
    A module that can help to get max performance of your laptop.
    Of course, if user's machine is a desktop it's pretty useless.
"""

import os

from sys import exit
from modules.logger import logger


class PerformanceHandler:
    """
        A class of machine performance handler.

        Attributes
        ----------
        performance_mode: str
            Current mode of cpu performance

        Methods
        -------
        boost(): void
            Boost system performance.
        powersave(): void
            Set powersave mode.
    """

    def __init__(self):
        with open("/sys/devices/system/cpu/cpu1/cpufreq/scaling_governor") as file:
            self.performance_mode = file.read()
        logger.log("Created an instance of the modules.performance_handler.PerformanceHandler class.")

    def boost(self):
        """ Boost machine performance. """
        os.system("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
        self.performance_mode = "performance"

        print("Set performance mode for your CPU.")
        exit()

    def powersave(self):
        """ Set powersave mode. """
        os.system("echo powersave | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
        self.performance_mode = "powersave"

        print("Set powersave mode for your CPU.")
        exit()
