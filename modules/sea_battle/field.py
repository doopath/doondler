""" A module of a playground field."""
from modules.logger import Logger
from modules.sea_battle.errors import HittingError

from modules.colors import to_red
from modules.colors import to_yellow
from modules.colors import to_white
from modules.colors import to_green

logger = Logger()


class Field:
    """
    A class of a playground field.
    It's a piece of the playground and can be blown up,
    busy by a ship and has an index like 'A1'.

    Attributes
    ----------
    index: str
        An index 'A1' format. Contains a letter and a digit; it's a coordinate of a ship.
    is_busy: bool (False by default)
        A marker that shows if the field is busy or not.
    is_blown_up: bool (False by default)
        A marker that shows if the field is busy or not.
    ship: Ship (None by default)
        A ship that located on this field (if it was located).
    marker: string (None by default)
        A marker of the field; It has a color and unique marker like "x", "=" or "#".
    is_hidden: bool
        Access or deny to show the field as well as it is.
        This attribute influences on the marker type.

    Methods
    -------
    clean(): void
        Clean a field and update current marker.
    hit(): str or void
        Destruct this field and destroy a ship located on this place.
        If it's already blown up then raise an error.
    locate(ship: Ship): void
        Set a ship on this field.
    """

    def __init__(self, index: str):
        self.index = index
        self.is_busy = False
        self.is_blown_up = False
        self.ship = None
        self.marker = None
        self.is_hidden = False
        self._set_marker()

    def _set_marker(self):
        if self.is_blown_up and self.is_busy:
            self.marker = to_red("x")
        if self.is_blown_up and not self.is_busy:
            self.marker = to_yellow("#")
        if not self.is_blown_up:
            self.marker = to_white("=")
        if self.is_hidden and not self.is_blown_up and self.is_busy:
            self.marker = to_white("=")
        if self.is_hidden and self.is_blown_up and not self.is_busy:
            self.marker = to_yellow("#")
        if not self.is_hidden and not self.is_blown_up and self.is_busy:
            self.marker = to_green("+")

    def _destruct(self):
        print(f"The {self.index} field was blown up.")
        self.is_blown_up = True
        self._set_marker()

    def clean(self):
        self.ship = None
        self.is_blown_up = False
        self.is_busy = False
        self._set_marker()

    def hit(self):
        """ Destroy a ship that is located at this field."""
        try:
            if not self.is_blown_up and self.is_busy:
                self._destruct()

                if False not in [f.is_blown_up for f in self.ship.fields]:
                    self.ship.destroy()

                    return "The ship was destroyed!"
                else:
                    return "Some ship at this field was damaged!"

            elif not self.ship and not self.is_blown_up:
                self._destruct()

                return "This is an empty field!"

            elif self.is_blown_up:
                raise HittingError("The field was already blown up!")

        except HittingError as error:
            logger.log(error)

    def locate(self, ship):
        self.ship = ship
        self.is_busy = True
        self._set_marker()

    def hide(self):
        self.is_hidden = True
