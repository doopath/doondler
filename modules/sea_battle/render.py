""" A module that renders the playground and other things. """
from os import system
from time import sleep
from modules.sea_battle.playground import Playground

from modules.colors import to_cyan

from threading import Thread
from modules.sea_battle.main import pg


class Checkbox:
    """
        A class of a checkbox with bool state property.
        Helps to stop some asynchronous loop.

        Attributes
        ----------
        _state: bool
            Main attribute that shows is the checkbox turned off or on.

        Methods
        -------
        turn_on(): void
            Turn on the checkbox.
        turn_off(): void
            Turn off the checkbox.
        get_state(): bool
            Get state of the checkbox.
    """

    def __init__(self):
        self._state: bool = False

    def turn_on(self):
        self._state = True

    def turn_off(self):
        self._state = False

    def get_state(self):
        return self._state


class RenderHandler:
    """
        A class that handles the game rendering.
        Of course the project does not support the rendering like separated window or
        something like that and anything will be rendered in terminal. But if you need to
        increase of decrease showing frames per second you can do it in the stream method
        by delay parameter - by default it equals 0.05s.

        Attributes
        ----------
        _is_clear: bool
            The mark that shows if the screen currently clear or not.
            Updating then something was shown or output was cleared.
        playground: Playground
            The gaming playground.
            Should be formatted with format() method at initialization.

        Methods
        -------
        render(): void
            Rendering the playground on the screen.
        stream(checkbox: Checkbox, delay: float = 0.05): void
            Start a multithreading stream that renders the playground while checkbox.state field is True.
            Stops to do it then checkbox.state field becomes False.
    """

    def __init__(self, playground: Playground):
        self._is_clear = False
        self.playground = playground
        self.playground.format()

    def _clear(self):
        system("clear")
        self._is_clear = True

    def _render_letter_coordinates(self, coordinates: list):
        print("    " + " ".join([to_cyan(c) for c in coordinates]))
        self._is_clear = False

    def _get_markers(self, row: list):
        return [f.marker for f in row]

    def _render_rows(self, rows: list):
        for row in rows:
            index = rows.index(row) + 1
            prefix = "  "
            fields = self._get_markers(row)

            if index > 9:
                prefix = " "

            print(str(prefix) + to_cyan(str(index)) + " " + " ".join(fields))

        self._is_clear = False

    def render(self):
        self._clear()
        self._render_letter_coordinates(self.playground.fields_list.keys())
        self._render_rows([row for letter, row in self.playground.fields_list.items()])
        self._is_clear = False

    def stream(self, checkbox: Checkbox, delay=0.05):
        while checkbox.get_state() is True:
            self.render()
            sleep(delay)


if __name__ == "__main__":
    rh = RenderHandler(pg)
    rh.render()
    sleep(1)
    pg.blow_up(pg.fields_list["C"][0].index)
    rh.render()

    # checkbox = Checkbox()
    # checkbox.turn_on()
    # thread = Thread(target=lambda: rh.render())
    # thread.start()
    # sleep(3)

    # for letter in pg.fields_list:
    #     for field in pg.fields_list[letter]:
    #         pg.blow_up(field.index)
    #         sleep(0.25)
