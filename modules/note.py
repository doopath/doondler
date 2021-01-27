""" User notification script (daemon) """
import os
import time

from sys import exit
from modules.logger import Logger
from modules.paths import get_path


logger = Logger()


def gen_note(deadline, author, message):
    """ Generate notification (create a .note_index file and remove it ad dead time). """
    note_content = "" \
                   "#!/usr/bin/env python3\n" \
                   '""" Doondler system notification. """\n'\
                   "import time\n" \
                   "import os\n" \
                   "import datetime\n" \
                   "\n\n" \
                   f"while {deadline} > round(time.time()):\n" \
                   "    time.sleep(1)\n\n" \
                   f"os.system('notify-send -t 0 \"{author}\" \"{message}\"')\n\n" \
                   f"logs = open('{get_path('logs')}', 'a')\n" \
                   "logs.write(f'[{str(datetime.datetime.now())[:19]}] - "\
                   f"Removed notification with id - {deadline}\\n')\n" \
                   f"logs.close()\n\n" \
                   f"os.remove(os.path.expanduser('~') + '/.note_{deadline}')\n" \
                   f"os.remove(os.path.expanduser('~') + '/.note_{deadline}_output')\n" \
                   "\n"

    return note_content


class Note:
    """ System notification. """

    def __init__(self, author, message, deadline=None, full_deadline=None):
        self.author = author
        self.message = message
        self.deadline = full_deadline or deadline
        self.fixed_deadline = bool(full_deadline)
        self.home_dir = get_path("home")

    def _set_deadline(self):
        if not self.fixed_deadline:
            self.deadline += round(time.time())

    def _make_note(self):
        return gen_note(self.deadline, self.author, self.message)

    def _exists(self):
        note = os.path.isfile(f"{get_path('note')}{self.deadline}")
        output = os.path.isfile(f"{get_path('note')}{self.deadline}_output")

        if note and output:
            return True

        return False

    def create(self):
        """ Create a notification and start a system daemon. """
        self._set_deadline()
        note_path = self.home_dir + "/.note_" + str(self.deadline)

        note = open(note_path, "w+")
        note.write(self._make_note())
        note.close()

        os.system(f"chmod +x {get_path('note')}{self.deadline}")
        os.system(f"nohup python3 -u {get_path('note')}{self.deadline} > "
                  f"{get_path('note')}{self.deadline}_output &")

        logger.log(f"Added a new note ({get_path('note')}{self.deadline})")

    def delete(self):
        """ Delete notification. """
        try:
            error_mes = f"Notification with id {self.deadline} does not exists!"
            assert self._exists() is True, error_mes

            os.remove(f"{get_path('note')}{self.deadline}")
            os.remove(f"{get_path('note')}{self.deadline}_output")

            logger.log(f"Removed notification with id = {self.deadline}")

        except AssertionError as error:
            logger.log(error)
            exit()


if __name__ == "__main__":
    Note("Yuigahama", "Yahallo!", 5).create()

