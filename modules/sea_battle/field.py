""" A module of a playground field."""
from modules.logger import Logger
from modules.sea_battle.errors import HitError

from modules.colors import to_red
from modules.colors import to_yellow
from modules.colors import to_white
from modules.colors import to_cyan

logger = Logger()


class Field:
    def __init__(self, index: str):
        self.index = index
        self.is_busy = False
        self.is_blown_up = False
        self.ship = None
        self.marker = None
        self._set_marker()

    def _set_marker(self):
        if self.is_blown_up and self.is_busy:
            self.marker = to_red("x")
        elif self.is_blown_up and not self.is_busy:
            self.marker = to_yellow("#")
        if not self.is_blown_up:
            self.marker = to_white("=")

    def clear(self):
        self.ship = None
        self.is_blown_up = False
        self.is_busy = False
        self._set_marker()

    def hit(self):
        """ Destroy a ship that is located at this field."""
        try:
            if not self.is_blown_up and self.is_busy:
                self.destruct()

                if False not in [f.is_blown_up for f in self.ship.fields]:
                    self.ship.destroy()

                    return "The ship was destroyed!"
                else:
                    return "Some ship at this field was damaged!"

            elif not self.ship and not self.is_blown_up:
                self.destruct()

                return "This is an empty field!"

            elif self.is_blown_up:
                raise HitError("The field was already blown up!")

        except HitError as error:
            logger.log(error)

    def destruct(self):
        print(f"The {self.index} field was blown up.")
        self.is_blown_up = True
        self._set_marker()

    def locate(self, ship):
        self.ship = ship
        self.is_busy = True
        self._set_marker()
