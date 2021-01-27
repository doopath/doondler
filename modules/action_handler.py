""" Action handler module """
import sys

from modules.logger import Logger
from modules.actions import actions


logger = Logger()


class ActionHandler:
    """
        A class of an actions handler.

        Parameters
        ----------
        args: list of strings
            List of given arguments.

        Methods
        -------
        reduce(): void
            Go throughout given arguments and execute them.

    """

    def __init__(self, system_args: list):
        self.args = system_args

    def _is_action(self, arg):
        if arg[:1] == "-":
            assert arg in actions, f"You gave incorrect parameter! Available actions list doesn't contains {arg}"
            return True

        return False

    def _get_action(self, arg: str):
        try:
            assert arg in actions, f"An action with name {arg} does not exists!"

            return actions[arg]

        except AssertionError as error:
            logger.log(error)
            exit()

    def _are_valid_args(self):
        """ Check if actinos are valid. """
        for action in self.args:
            for subaction in self.args:
                is_same_indexes = self.args.index(action) == self.args.index(subaction)
                is_same_means = action == subaction

                if not is_same_indexes and is_same_means and self._is_action(action):
                    return False

                if self._is_action(action) and action not in self.args:
                    return False

        return True

    def _get_action_parameters(self, action: dict, parameters_count: int):
        action_index = self.args.index(action)

        return self.args[action_index+1:action_index+parameters_count+1]

    def reduce(self):
        """ Run throughout actions and execute them. """
        try:
            for arg in self.args:
                assert self._are_valid_args(), "You gave incorrect actions!"

                if self._is_action(arg):
                    action = self._get_action(arg)
                    action_parameters_count = action["arguments"]
                    action_parameters = self._get_action_parameters(
                        action["option"],
                        action_parameters_count)

                    assert len(action_parameters) is action_parameters_count, ""\
                        f"Action {action['option']} expected {action_parameters_count} "\
                        f"arguments, but got {len(action_parameters)}!"

                    action["action"](*action_parameters)

        except AssertionError as error:
            logger.log(error)
            sys.exit()
