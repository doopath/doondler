""" A module of a playground. """
import string
from sys import exit
from time import sleep

from modules.logger import Logger

from modules.sea_battle.field import Field
from modules.sea_battle.ship import Ship
from modules.sea_battle.errors import FillingError

from modules.sea_battle.errors import PlaygroundValidationError


logger = Logger()


class Playground:
    def __init__(self):
        self.fields_list = {}
        self.columns_count = 9
        self.rows_count = 9
        self.validator = PlaygroundValidator(self)

    def _make_row(self, letter: str):
        self.fields_list[letter.upper()] = [Field(letter.upper()+str(i)) for i in range(1, self.columns_count+1)]

    def create(self):
        for i in range(self.rows_count):
            self._make_row(string.ascii_lowercase[i])

    def overwrite(self, pos: tuple, target: Field):
        self.fields_list[pos[0]][pos[1]] = target

    def fill(self, ships: list):
        for ship in ships:
            for field in ship.fields:
                self.fields_list[field.index.upper()[:1]][int(field.index[1:])-1].locate(ship)

            self.validator.validate(ship)

    def blow_up(self, index):
        return self.fields_list[index.upper()[:1]][int(index[1:])-1].hit()

    def validate(self):
        ships = []
        [[ships.append(item.ship) for item in sublist] for sublist in [couple[1] for couple in self.fields_list.items()]]
        ships = filter(lambda ship: True if ship is not None else False, ships)
        [self.validator.validate(ship) for ship in ships]

    def format(self):
        letters = string.ascii_uppercase

        for letter in self.fields_list.keys():
            for i in range(len(self.fields_list[letter])):
                target_letter = letters[i]

                buffer = self.fields_list[letter][i]
                target = self.fields_list[target_letter][letters.index(letter)]

                self.overwrite((buffer.index[0], int(buffer.index[1])-1), target)
                self.overwrite((target.index[0], int(target.index[1])-1), buffer)


class PlaygroundValidator:
    def __init__(self, playground: Playground):
        self.fields_list = playground.fields_list

    def _are_valid_fields(self, ship: Ship):
        fields = ship.fields
        coordinates = list(string.ascii_uppercase)

        try:
            for i in range(len(fields) - 1):
                if int(fields[i].index[1]) + 1 != int(fields[i + 1].index[1]):
                    if coordinates[coordinates.index(fields[i].index[0]) + 1] != ship.fields[i + 1].index[0]:
                        raise FillingError(
                            f"You cannot create a ship with coordinates {str([f.index for f in fields])}")

        except FillingError as error:
            logger.log(error)

    def _vertical_validation(self, fields: list, field: Field):
        c_letters = string.ascii_uppercase
        letter = field.index[0]
        digit = field.index[1:]
        fields_to_check = []

        next_index = fields[fields.index(field) + 1].index if fields.index(field) != len(fields) - 1 else None
        is_first = True if fields.index(field) == 0 else False

        if digit != "1" and is_first:
            fields_to_check.append(self.fields_list[letter][int(digit)-2])
        if digit != str(len(self.fields_list)) and next_index is None:
            fields_to_check.append(self.fields_list[letter][int(digit)])
        if letter != "A":
            fields_to_check.append(self.fields_list[c_letters[c_letters.index(letter)-1]][int(digit)-1])
        if letter != list(self.fields_list)[-1]:
            fields_to_check.append(self.fields_list[c_letters[c_letters.index(letter)+1]][int(digit)-1])

        return fields_to_check

    def _horizontal_validation(self, fields: list, field: Field):
        c_letters = string.ascii_uppercase
        letter = field.index[0]
        digit = field.index[1:]
        fields_to_check = []

        next_index = fields[fields.index(field) + 1].index if fields.index(field) != len(fields) - 1 else None
        is_first = True if fields.index(field) == 0 else False

        def get_letter(pos: str): return c_letters[c_letters.index(letter) + (1 if pos == "next" else (-1))]

        if letter != "A" and is_first:
            fields_to_check.append(self.fields_list[get_letter("prev")][int(digit)-1])
        if letter != list(self.fields_list)[-1] and next_index is None:
            fields_to_check.append(self.fields_list[get_letter("next")][int(digit)-1])
        if digit != "1":
            fields_to_check.append(self.fields_list[letter][int(digit)])
        if digit != str(len(self.fields_list)):
            fields_to_check.append(self.fields_list[letter][int(digit)-2])

        return fields_to_check

    def _is_valid_location(self, ship):
        fields = ship.fields

        try:
            def get_location_type():
                if len(set([f.index[0] for f in fields])) == 1:
                    return "vertical"
                elif len(set([f.index[1:] for f in fields])) == 1:
                    return "horizontal"
                else:
                    raise PlaygroundValidationError(f"The ship at fields {[f.index for f in fields]} is incorrect!")

            fields_to_check = []
            if len(fields) > 1:
                location_type = get_location_type()

                for field in fields:
                    if location_type == "vertical":
                        fields_to_check += self._vertical_validation(fields, field)
                    if location_type == "horizontal":
                        fields_to_check += self._horizontal_validation(fields, field)

            for field in fields_to_check:
                if field.is_busy:
                    raise PlaygroundValidationError(f"The ship at fields {[f.index for f in fields]} is incorrect!")

        except PlaygroundValidationError as error:
            logger.log(error)
            ship.unset()
            logger.log(f"The ship at fields {[f.index for f in fields]} was unset.")

    def validate(self, ship: Ship):
        self._are_valid_fields(ship)
        self._is_valid_location(ship)


if __name__ == "__main__":
    pg = Playground()
    pg.create()
