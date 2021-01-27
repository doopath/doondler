""" System handler Yuigahama """
import sys

from modules.note import Note
from modules.logger import Logger

logger = Logger()


class Handler:
    """ Yuigahama handler """
    name = "yuigahama"

    def __init__(self, user):
        self.master = user
        self.name = "yuigahama"

    def _convert_interval(self, interval):
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

        except Exception as error:
            logger.log(error)
            sys.exit()

    def greet(self):
        """ Greet to user """
        print(f"Yahallo, {self.master.username}")


if __name__ == "__main__":
    yui = Handler("Michael")
    yui.make_note("Do not forget to go to the shop.", "5m")

