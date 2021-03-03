""" A module of the playground. """
import string

from sys import exit

from modules.logger import Logger

from modules.sea_battle.field import Field
from modules.sea_battle.ship import Ship

from modules.sea_battle.errors import FillingError
from modules.sea_battle.errors import PlaygroundValidationError

logger = Logger()


class Playground:
    """
    A class of the playground.

    Attributes
    ----------
    fields_list: dict
        A dictionary contains letter: [fields].
    columns_count: int
        A count of columns: horizontal columns - digits.
    rows_count: int
        A count of rows: vertical row - letters.
    validator: PlaygroundValidator
        A Validator with a method validate getting a ship and checking it.
    is_hidden: bool
        Access or deny to show playground fields.

    Methods
    -------
    create(): void
        Create a playground.
    fill(ships: list): void
        Fill the playground with ships.
    overwrite(pos: tuple, target: Field): void
        Overwrite a field at position pos with the target field.
    blow_up(index: str): str
        Blow up a field with index=index.
    validate(): void
        Validate current playground.
    format(): void
        Format current playground to playable form.
    """

    def __init__(self, is_hidden=False):
        self.fields_list = {}
        self.columns_count = 9
        self.rows_count = 9
        self.validator = PlaygroundValidator(self)
        self.is_hidden = is_hidden

    def _make_row(self, letter: str):
        self.fields_list[letter.upper()] = [Field(letter.upper() + str(i)) for i in range(1, self.columns_count + 1)]

    def _hide_field(self, field: Field):
        if self.is_hidden:
            field.hide()

    def create(self):
        """ Create an empty playground. """
        for i in range(self.rows_count):
            self._make_row(string.ascii_lowercase[i])

    def overwrite(self, pos: tuple, target: Field):
        """ Overwrite a field at position=pos with field=target. """
        self.fields_list[pos[0]][pos[1]] = target

    def fill(self, ships: list):
        """ Fill the playground with ships. """
        for ship in ships:
            for field in ship.fields:
                self.fields_list[field.index.upper()[:1]][int(field.index[1:]) - 1].locate(ship)
                self._hide_field(field)

            self.validator.validate(ship)

    def blow_up(self, index: str):
        """ Blow up some ship and index=index. """
        return self.fields_list[index.upper()[0]][int(index[1:]) - 1].hit()

    def validate(self):
        """ Validate the full playground. """
        ships = []
        [[ships.append(item.ship) for item in sublist] for sublist in
         [couple[1] for couple in self.fields_list.items()]]
        ships = filter(lambda ship: True if ship is not None else False, ships)
        [self.validator.validate(ship) for ship in ships]

    def format(self):
        """
        Format the current playground.
        It's require to correct rendering.
        """

        letters = string.ascii_uppercase

        for letter in self.fields_list.keys():
            for i in range(len(self.fields_list[letter])):
                target_letter = letters[i]

                buffer = self.fields_list[letter][i]
                target = self.fields_list[target_letter][letters.index(letter)]

                self.overwrite((buffer.index[0], int(buffer.index[1]) - 1), target)
                self.overwrite((target.index[0], int(target.index[1]) - 1), buffer)


class PlaygroundValidator:
    """
    A class of the playground validator.

    Attributes
    ----------
    fields_list: dict {"Letter": list}
        A list of fields. Get those from the playground attribute - playground.fields_list.

    Methods
    -------
    validate(ship: Ship): void
        Validate a location of some ship and raise a validation error if it is incorrect.
    """

    def __init__(self, playground: Playground):
        self.fields_list = playground.fields_list
        self._c_letters = string.ascii_uppercase
        self._fields_to_check = []

        self._horizontal_validator = HorizontalValidator(playground)
        self._vertical_validator = VerticalValidator(playground)
        self._diagonal_validator = DiagonalValidator(playground)

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

    def _direction_validation(self, validator, fields: list, field: Field, direction_type: str):
        validator.set_direction_type(direction_type)
        validator.validate(fields, field)
        self._fields_to_check += validator.get_fields()
        validator.empty_fields()

    def _clear_fields_to_check(self):
        self._fields_to_check = []

    def _is_valid_location(self, ship):
        fields = ship.fields

        try:
            def get_direction_type():
                if len(set([f.index[0] for f in fields])) == 1:
                    return "vertical"
                elif len(set([f.index[1:] for f in fields])) == 1:
                    return "horizontal"
                else:
                    raise PlaygroundValidationError(f"The ship at fields {[f.index for f in fields]} is incorrect!")

            if len(fields) > 1:
                direction_type = get_direction_type()

                for field in fields:
                    if direction_type == "vertical":
                        self._direction_validation(self._vertical_validator, fields, field, direction_type)
                    if direction_type == "horizontal":
                        self._direction_validation(self._horizontal_validator, fields, field, direction_type)

                    self._direction_validation(self._diagonal_validator, fields, field, direction_type)

            for i in range(len(self._fields_to_check)):
                field = self._fields_to_check.pop(0)

                if field.is_busy:
                    raise PlaygroundValidationError(f"The ship at fields {[f.index for f in fields]} is incorrect!")

        except PlaygroundValidationError as error:
            logger.log(error)
            ship.unset()
            self._clear_fields_to_check()
            logger.log(f"The ship at fields {[f.index for f in fields]} was unset.")

    def validate(self, ship: Ship):
        """ Validate a ship and raise a validation error if it's incorrect. """
        self._are_valid_fields(ship)
        self._is_valid_location(ship)


class DirectionValidator:
    """
    A class of a validator by some direction (horizontal, vertical).
    Every 'Validator' (child of this class) has four public methods (see Methods).

    Attributes
    ----------
    fields_list: dict{"Letter": [Field]}
        A list of playground fields.
    _c_letters: list[str]
        A list of ascii uppercase letters.
    _fields_to_check: list[Field]
        A list of fields which should be checked.
    _direction_type: str
        A type of direction to validation (horizontal, vertical).

    Methods
    -------
    get_fields(): list[Field]
        Get a list with 'fields_to_check'.
    empty_fields(): void
        Empty a list with 'fields_to_check'.
    set_direction_type(_type: str): void
        Set a type for direction (horizontal, vertical).
    validate(fields: list[Field], field: Field): void
        Go through any ship's fields and add to the 'fields to check' list those may conflict with others.
        Gets two arguments:
            fields - list of current ship's fields;
            field - current validating field.
    """

    def __init__(self, playground: Playground):
        self.fields_list = playground.fields_list
        self._c_letters = string.ascii_uppercase
        self._fields_to_check = []
        self._direction_type = None

    def _get_letter(self, position: str, current_letter: str):
        index = 0

        if position == "next":
            index = 1
        elif position == "prev":
            index = -1

        return self._c_letters[self._c_letters.index(current_letter) + index]

    def _pick_letter(self, field: Field):
        return field.index[0]

    def _pick_digit(self, field: Field):
        return field.index[1:]

    def _is_first_field(self, fields: list, field: Field):
        return True if fields.index(field) == 0 else False

    def _is_last_field(self, fields: list, field: Field):
        return True if fields.index(field) == len(fields) - 1 else False

    def _add_side_field(self, digit: str, letter: str, side: str):
        pass

    def get_fields(self):
        return self._fields_to_check

    def empty_fields(self):
        self._fields_to_check = []

    def set_direction_type(self, _type: str):
        self._direction_type = _type

    def validate(self, fields: list, field: Field):
        pass


class VerticalValidator(DirectionValidator):
    def _add_side_field(self, digit: str, letter: str, side: str):
        if side == "left" or side == "right":
            offset = -1 if side == "left" else 1
            self._fields_to_check.append(
                self.fields_list[self._c_letters[self._c_letters.index(letter) + offset]][int(digit) - 1])
        if side == "top" or side == "bottom":
            offset = -2 if side == "top" else 0
            self._fields_to_check.append(self.fields_list[letter][int(digit) + offset])

    def validate(self, fields: list, field: Field):
        letter = self._pick_letter(field)
        digit = self._pick_digit(field)

        is_first = self._is_first_field(fields, field)
        is_last = self._is_last_field(fields, field)

        if digit != "1" and is_first:
            self._add_side_field(digit, letter, "top")

        if digit != str(len(self.fields_list)) and is_last:
            self._add_side_field(digit, letter, "bottom")

        if letter != "A":
            self._add_side_field(digit, letter, "left")

        if letter != list(self.fields_list)[-1]:
            self._add_side_field(digit, letter, "right")


class HorizontalValidator(DirectionValidator):
    def _add_side_field(self, digit: str, letter: str, side: str):
        if side == "prev" or side == "next":
            self._fields_to_check.append(self.fields_list[self._get_letter(side, letter)][int(digit) - 1])
        if side == "top" or side == "bottom":
            offset = -2 if side == "top" else 0
            self._fields_to_check.append(self.fields_list[letter][int(digit) + offset])

    def validate(self, fields: list, field: Field):
        letter = self._pick_letter(field)
        digit = self._pick_digit(field)

        is_last = self._is_last_field(fields, field)
        is_first = self._is_first_field(fields, field)

        if letter != "A" and is_first:
            self._add_side_field(digit, letter, "prev")

        if letter != list(self.fields_list)[-1] and is_last:
            self._add_side_field(digit, letter, "next")

        if digit != "1":
            self._add_side_field(digit, letter, "top")

        if digit != str(len(self.fields_list)):
            self._add_side_field(digit, letter, "bottom")


class DiagonalValidator(DirectionValidator):
    def _add_side_field(self, digit: str, letter: str, offset: tuple):
        self._fields_to_check.append(
            self.fields_list[self._c_letters[self._c_letters.index(letter) + offset[0]]][int(digit) + offset[1]])

    def validate(self, fields: list, field: Field):
        letter = self._pick_letter(field)
        digit = self._pick_digit(field)

        is_last = self._is_last_field(fields, field)
        is_first = self._is_first_field(fields, field)

        if self._direction_type == "vertical":
            if letter != "A" and is_first and digit != "1":
                self._add_side_field(digit, letter, (-1, -2))

            if letter != list(self.fields_list)[-1] and is_first and digit != "1":
                self._add_side_field(digit, letter, (1, -2))

            if digit != str(len(self.fields_list)) and is_last and letter != "A":
                self._add_side_field(digit, letter, (-1, 0))

            if digit != str(len(self.fields_list)) and is_last and letter != list(self.fields_list)[-1]:
                self._add_side_field(digit, letter, (1, 0))

        if self._direction_type == "horizontal":
            if letter != "A" and digit != "1" and is_first:
                self._add_side_field(digit, letter, (-1, -2))

            if letter != list(self.fields_list)[-1] and digit != "1" and is_last:
                self._add_side_field(digit, letter, (1, -2))

            if letter != "A" and digit != str(len(self.fields_list)) and is_first:
                self._add_side_field(digit, letter, (-1, 0))

            if letter != list(self.fields_list)[-1] and digit != str(len(self.fields_list)) and is_last:
                self._add_side_field(digit, letter, (1, 0))
