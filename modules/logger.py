""" Handling of exceptions """
from os import path
import datetime
import traceback
from modules.colors import yellow
from modules.colors import no_color
from modules.paths import get_path


class Logger:
    """ Logger of errors and events """
    def __init__(self, log_path=get_path("logs")):
        self.log_path = log_path

    def _get_log_date(self):
        return str(datetime.datetime.now())[:19]

    def _write_log(self, log):
        current_time = self._get_log_date()

        log_file = open(self.log_path, "a")
        log_file.write(f"[{current_time}] - {log}\n")
        log_file.close()

    def log(self, error):
        """ Logging an error into .doondler_logs file (at home directory). """
        self._write_log(error)

        print(f"{yellow}{error}{no_color}")

        if error is Exception:
            traceback.print_exc()

