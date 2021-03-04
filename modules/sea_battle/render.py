""" A module that renders the playground and other things. """
from os import system
from time import sleep
from threading import Thread

from modules.sea_battle.playground import Playground
from modules.colors import to_cyan
from modules.sea_battle.main import ships, pg


class RenderHandler:
    """
        A class that handles the game rendering.
        Of course the project does not support the rendering like separated window or
        something like that and anything will be rendered in terminal. But if you need to

        Attributes
        ----------
        playground: Playground
            The gaming playground.
            Should be formatted with format() method at initialization.

        Properties
        ----------
        output: str
            An output string that has been prepared for you :>

        Methods
        -------
        render(): void (IO)
            Returns a string that contains two playgrounds and their coordinates.
        format_playgrounds(): void
            Format using playgrounds (enemy's and user's ones).
    """

    def __init__(self, user_playground: Playground, enemy_playground: Playground):
        self._output = "\n\t\t--> Your and enemy's playgrounds <--\n\n"
        self.user_playground = user_playground
        self.enemy_playground = enemy_playground

        self._validate_playgrounds()

    def _validate_playgrounds(self):
        same_keys = self.user_playground.fields_list.keys() == self.enemy_playground.fields_list.keys()
        assert same_keys, "Letters in the user playground should be equal letters of the enemy playground!"

        for letter in self.user_playground.fields_list.keys():
            same_length = len(self.user_playground.fields_list[letter]) == len(self.enemy_playground.fields_list[letter])
            assert same_length, "Length of every item in two playgrounds should be same!"

    def _get_coordinates(self):
        coordinates = to_cyan(" ".join(self.user_playground.fields_list.keys()))

        return "\t  " + coordinates + "\t\t\t" + "  " + coordinates + "\n"

    def _get_markers(self, fields_list: list):
        return [field.marker for field in fields_list]

    def _get_user_playground_markers(self, index: int, letter: str):
        return "\t" + to_cyan(str(index)) + " " + " ".join(
            self._get_markers(self.user_playground.fields_list[letter]))

    def _get_enemy_playground_markers(self, index: int, letter: str):
        return to_cyan(str(index)) + " " + " ".join(
            self._get_markers(self.enemy_playground.fields_list[letter]))

    def _prepare_output(self):
        self._output += self._get_coordinates()
        index = 1

        for letter in self.user_playground.fields_list.keys():
            self._output += self._get_user_playground_markers(index, letter) + "\t\t\t" +\
                self._get_enemy_playground_markers(index, letter) + "\n"
            index += 1

        self._output += "\n\n"

    def format_playgrounds(self):
        self.user_playground.format()
        self.enemy_playground.format()

    @property
    def output(self):
        return self._output

    def render(self):
        system("clear")
        self._prepare_output()
        print(self._output)


def beta_render():
    pg.fill(ships)
    pg.validate()
    render_handler = RenderHandler(pg, pg)
    render_handler.format_playgrounds()
    render_handler.render()

if __name__ == "__main__":
    beta_render()
