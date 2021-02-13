""" A module of a playground. """
import string
from sys import exit
from modules.logger import Logger
from modules.sea_battle.field import Field
from modules.sea_battle.ship import Ship
from modules.sea_battle.errors import FillingError


logger = Logger()


class Playground:
    def __init__(self):
        self.fields_list = {}
        self.columns_count = 10
        self.rows_count = 10

    def _make_row(self, letter: str):
        self.fields_list[letter.upper()] = [Field(letter.upper()+str(i)) for i in range(1, self.columns_count+1)]

    def create(self):
        for i in range(self.rows_count):
            self._make_row(string.ascii_lowercase[i])

    def _are_valid_fields(self, ship: Ship):
        fields = ship.fields
        coordinates = list(string.ascii_uppercase)

        try:
            for i in range(len(fields)-1):
                if int(fields[i].index[1])+1 != int(fields[i+1].index[1]):
                    if coordinates[coordinates.index(fields[i].index[0])+1] != ship.fields[i+1].index[0]:
                        raise FillingError(f"You cannot create a ship with coordinates {str([f.index for f in fields])}")

        except FillingError as error:
            logger.log(error)
            exit()

    def fill(self, ships: list):
        for ship in ships:
            self._are_valid_fields(ship)

            for field in ship.fields:
                self.fields_list[field.index.upper()[:1]][int(field.index[1:])-1].locate(ship)

    def blow_up(self, index):
        return self.fields_list[index.upper()[:1]][int(index[1:])-1].hit()


if __name__ == "__main__":
    pg = Playground()
    pg.create()
