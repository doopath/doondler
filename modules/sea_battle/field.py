""" A module of a playground field."""
from modules.logger import Logger
from modules.sea_battle.errors import HitError


logger = Logger()


class Field:
    def __init__(self, index: str):
        self.index = index
        self.is_busy = False
        self.is_blown_up = False
        self.ship = None

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

    def locate(self, ship):
        self.ship = ship
        self.is_busy = True
