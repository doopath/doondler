""" System handler Yuigahama """
import sys

from modules.note import Note
from modules.logger import logger


class Handler:
    """ Yuigahama handler """
    name = "yuigahama"

    def __init__(self, user):
        self.master = user
        self.name = "yuigahama"
        logger.log("An instance of the modules.yuigahama.Handler was made.")

    def _convert_interval(self, interval: str) -> int:
        ext = interval[-1]  # s or m or h (seconds, minutes, hours).
        interval = int(str(interval)[:-1])  # Default = seconds.

        if ext == "s":
            pass
        elif ext == "m":
            interval *= 60
        elif ext == "h":
            interval *= 3600
        else:
            raise AssertionError("You've given an incorrect note deadline! (only s/m/h)")

        return interval

    def make_note(self, message, interval=None, deadline=None):
        """ Make a notification while current session running """
        try:
            name = self.name[0].upper() + self.name[1:]

            if interval:
                interval = self._convert_interval(interval)

            message = "Master, you asked me to remind you:\\n" + message
            note = Note(name, message, interval, full_deadline=deadline)
            note.create()
            logger.log("Created a note at the modules.yuigahama.Handler. Should be "
                       f"removed at {deadline}.")


        except Exception as error:
            logger.log(error)
            sys.exit()
