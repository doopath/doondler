""" Handling of exceptions """
import datetime
import traceback

from modules.errors import Warning
from modules.colors import red, yellow, white
from modules.colors import no_color
from modules.paths import get_path


class Logger:
    """
    A class of the logger that handles errors, warns and notices.

    Attributes
    ----------
    log_path: str = get_path("logs")
        A path to the log file (by default it is /home/user/.doondler_logs).
    enable_traceback: bool = False
        Enable or disable showing a traceback for errors.
    log_level: int = 2
        A level that filter any input stuff and passes only allowed.
        For example, if you set 3 log level then it passes any input info
        and shows it. But if you set 2 log level then it won't pass notices
        (only errors and warningss).
        1 - only errors;
        2 - errors and warnings;
        3 - any stuff.

    Methods
    -------
    log(error: Exception or str) -> None
        Log an error, warn or notice to the log file.
    set_log_level(new_log_level: int) -> None
        Set new log level.
    set_traceback_showing_mode(mode: bool) -> None
        Set a mode (True or False) for showing a traceback.
    """

    def __init__(self, log_path: str = get_path("logs"), log_level: int = 2, enable_traceback: bool = True):
        self.log_path = log_path
        self.log_level = log_level
        self.enable_traceback = enable_traceback

    def _get_log_date(self):
        return str(datetime.datetime.now())[:19]

    def _write_log(self, log):
        current_time = self._get_log_date()

        log_file = open(self.log_path, "a")
        log_file.write(f"[{current_time}] - {log}\n")
        log_file.close()

    def _log_error(self, error: Exception):
        self._write_log(error)
        print(f"\n{red}{error}{no_color}")

        if self.enable_traceback:
            traceback.print_exc()

    def _log_warning(self, warning: Warning):
        if self.log_level >= 2:
            self._write_log(warning)
            print(f"{yellow}{warning}{no_color}")

    def _log_notice(self, notice: str):
        if self.log_level == 3:
            self._write_log(notice)
            print(f"{white}{notice}{no_color}")

    def log(self, error):
        """ Log an error, warn or notice to the log file. """
        if isinstance(error, str):
            self._log_notice(error)
        elif isinstance(error, Warning):
            self._log_warning(error)
        elif isinstance(error, Exception):
            self._log_error(error)
        else:
            raise TypeError("You gave something incorrect to the log method!")

    def set_log_level(self, new_log_level: int):
        """ Set new log level. """
        assert 4 > new_log_level > 0, f"The log level with value: {new_log_level} is incorrect!"
        assert new_log_level is int, f"Log level is an integer, not {type(new_log_level)}"

        self.log_level = new_log_level

    def set_traceback_showing_mode(self, mode: bool):
        assert mode is not bool, "The mode of showing traceback may be only boolean type!"
        self.enable_traceback = mode


logger = Logger()
